from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

router = APIRouter()


class ErrorLogRequest(BaseModel):
    moduleId: str
    errorCode: str | None = None
    message: str
    stack: str | None = None
    context: dict[str, Any] = {}
    severity: str = "error"  # "debug" | "info" | "warning" | "error" | "critical"
    userId: str | None = None


# ---------------------------------------------------------------------------
# POST /errors/log
# ---------------------------------------------------------------------------
@router.post("/log", status_code=201)
async def log_error(body: ErrorLogRequest):
    """
    Logs an error from any Now ecosystem module.
    Placeholder — Supabase insert will go here once tables are created.

    Table: error_logs (id, moduleId, errorCode, message, stack, context, severity,
                       userId, occurred_at)
    """
    # TODO:
    # db.get_db().table("error_logs").insert({
    #     "moduleId": body.moduleId,
    #     "errorCode": body.errorCode,
    #     "message": body.message,
    #     "stack": body.stack,
    #     "context": body.context,
    #     "severity": body.severity,
    #     "userId": body.userId,
    #     "occurred_at": "now()",
    # }).execute()
    return {"status": "logged", "moduleId": body.moduleId, "severity": body.severity}
