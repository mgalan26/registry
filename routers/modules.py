from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any

router = APIRouter()


class OperationDef(BaseModel):
    name: str
    description: str | None = None
    path: str
    method: str = "POST"


class RegisterModuleRequest(BaseModel):
    moduleId: str
    baseUrl: str
    version: str
    operations: list[OperationDef]
    dependencies: list[str] = []
    metadata: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# POST /modules/register
# ---------------------------------------------------------------------------
@router.post("/register", status_code=201)
async def register_module(body: RegisterModuleRequest):
    """
    Registers a module with its operations and dependencies.
    Placeholder — Supabase upsert will go here once tables are created.

    Table: modules (moduleId, baseUrl, version, operations, dependencies, metadata, registered_at)
    """
    # TODO: db.get_db().table("modules").upsert({...}).execute()
    return {
        "status": "registered",
        "moduleId": body.moduleId,
        "version": body.version,
    }


# ---------------------------------------------------------------------------
# GET /modules/{moduleId}/resolve/{operationName}
# ---------------------------------------------------------------------------
@router.get("/{moduleId}/resolve/{operationName}")
async def resolve_operation(moduleId: str, operationName: str):
    """
    Returns the concrete endpoint URL for a given operation of a module.
    Placeholder — Supabase select will go here once tables are created.

    Query: modules where moduleId = moduleId, then find operation by name.
    """
    # TODO:
    # row = db.get_db().table("modules").select("*").eq("moduleId", moduleId).single().execute()
    # if not row.data: raise HTTPException(404, "Module not found")
    # op = next((o for o in row.data["operations"] if o["name"] == operationName), None)
    # if not op: raise HTTPException(404, "Operation not found")
    # return {"endpoint": row.data["baseUrl"] + op["path"], "method": op["method"]}
    raise HTTPException(status_code=501, detail="Not implemented — awaiting Supabase tables")


# ---------------------------------------------------------------------------
# GET /modules/status
# ---------------------------------------------------------------------------
@router.get("/status")
async def modules_status():
    """
    Returns the registration status of all modules.
    Placeholder — Supabase select will go here once tables are created.

    Query: SELECT moduleId, version, registered_at FROM modules ORDER BY registered_at DESC
    """
    # TODO: rows = db.get_db().table("modules").select("moduleId, version, registered_at").execute()
    # return {"modules": rows.data}
    return {"modules": [], "note": "Awaiting Supabase tables"}
