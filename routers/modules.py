from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, model_validator
from typing import Any, Optional

from db import get_db

router = APIRouter()


class OperationDef(BaseModel):
    nombre: Optional[str] = None
    name: Optional[str] = None
    endpoint: Optional[str] = None
    path: Optional[str] = None
    metodo: Optional[str] = None
    method: Optional[str] = None
    descripcion: Optional[str] = None
    description: Optional[str] = None

    @model_validator(mode="after")
    def normalize(self):
        self.name = self.name or self.nombre
        self.path = self.path or self.endpoint
        self.method = (self.method or self.metodo or "POST").upper()
        if not self.name:
            raise ValueError("Operation requires 'name' or 'nombre'")
        if not self.path:
            raise ValueError("Operation requires 'path' or 'endpoint'")
        return self


class RegisterModuleRequest(BaseModel):
    moduleId: str
    endpoint_base: Optional[str] = None
    baseUrl: Optional[str] = None
    nombre: Optional[str] = None
    version: str
    operations: list[OperationDef]
    dependencies: list[str] = []
    metadata: dict[str, Any] = {}

    @model_validator(mode="after")
    def normalize(self):
        self.baseUrl = self.baseUrl or self.endpoint_base
        if not self.baseUrl:
            raise ValueError("Requires 'baseUrl' or 'endpoint_base'")
        return self


# ---------------------------------------------------------------------------
# POST /modules/register
# ---------------------------------------------------------------------------
@router.post("/register", status_code=201)
async def register_module(body: RegisterModuleRequest):
    try:
        db = get_db()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"DB init error: {e}")

    try:
        db.table("modulos").upsert({
            "id": body.moduleId,
            "nombre": body.nombre or body.moduleId,
            "version": body.version,
            "endpoint_base": body.baseUrl,
            "estado": "activo",
        }).execute()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"modulos upsert error: {e}")

    if body.operations:
        ops = [
            {
                "modulo_id": body.moduleId,
                "nombre": op.name,
                "endpoint": op.path,
                "metodo": op.method,
                "descripcion": op.descripcion or op.description,
                "version": body.version,
            }
            for op in body.operations
        ]
        try:
            db.table("operaciones").upsert(ops, on_conflict="modulo_id,nombre").execute()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"operaciones upsert error: {e}")

    return {
        "status": "registered",
        "moduleId": body.moduleId,
        "version": body.version,
        "operations": len(body.operations),
    }


# ---------------------------------------------------------------------------
# GET /modules/status  — debe ir ANTES de /{moduleId}/...
# ---------------------------------------------------------------------------
@router.get("/status")
async def modules_status():
    db = get_db()
    result = db.table("modulos").select("id, nombre, version, estado, registered_at").execute()
    return {"modules": result.data}


# ---------------------------------------------------------------------------
# GET /modules/{moduleId}/resolve/{operationName}
# ---------------------------------------------------------------------------
@router.get("/{moduleId}/resolve/{operationName}")
async def resolve_operation(moduleId: str, operationName: str):
    db = get_db()

    mod = db.table("modulos").select("endpoint_base, estado").eq("id", moduleId).maybe_single().execute()
    if not mod.data:
        raise HTTPException(status_code=404, detail=f"Module '{moduleId}' not found")

    op = (
        db.table("operaciones")
        .select("endpoint, metodo")
        .eq("modulo_id", moduleId)
        .eq("nombre", operationName)
        .maybe_single()
        .execute()
    )
    if not op.data:
        raise HTTPException(status_code=404, detail=f"Operation '{operationName}' not found in module '{moduleId}'")

    return {
        "endpoint": mod.data["endpoint_base"] + op.data["endpoint"],
        "method": op.data["metodo"],
    }
