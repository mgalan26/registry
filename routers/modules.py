from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, model_validator
from typing import Any, Optional

router = APIRouter()


class OperationDef(BaseModel):
    # Acepta campos en español o inglés
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
    # Acepta endpoint_base (español) o baseUrl (inglés)
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
    # TODO: db.get_db().table("modulos").upsert({
    #   "id": body.moduleId,
    #   "nombre": body.nombre or body.moduleId,
    #   "version": body.version,
    #   "endpoint_base": body.baseUrl,
    #   "estado": "activo",
    # }).execute()
    # + upsert operaciones
    return {
        "status": "registered",
        "moduleId": body.moduleId,
        "version": body.version,
    }


# ---------------------------------------------------------------------------
# GET /modules/status  — debe ir ANTES de /{moduleId}/...
# ---------------------------------------------------------------------------
@router.get("/status")
async def modules_status():
    # TODO: rows = db.get_db().table("modulos").select("id, nombre, version, estado, registered_at").execute()
    return {"modules": [], "note": "Awaiting Supabase tables"}


# ---------------------------------------------------------------------------
# GET /modules/{moduleId}/resolve/{operationName}
# ---------------------------------------------------------------------------
@router.get("/{moduleId}/resolve/{operationName}")
async def resolve_operation(moduleId: str, operationName: str):
    # TODO: query modulos + operaciones
    raise HTTPException(status_code=501, detail="Not implemented — awaiting Supabase tables")
