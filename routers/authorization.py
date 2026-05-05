from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class CheckAuthRequest(BaseModel):
    requestingModule: str
    owningModule: str
    userId: str
    operation: str


class GrantAuthRequest(BaseModel):
    userId: str
    module: str
    operations: list[str] = []
    grantedBy: str | None = None


# ---------------------------------------------------------------------------
# POST /auth/check
# ---------------------------------------------------------------------------
@router.post("/check")
async def check_authorization(body: CheckAuthRequest):
    """
    checkAuthorization(requestingModule, owningModule, userId, operation)
    Returns authorized: true/false.
    Placeholder — Supabase select will go here once tables are created.

    Table: authorizations (userId, module, operations[], granted_at, granted_by)
    Query: authorizations where userId = userId AND module = owningModule
           AND operation IN operations[]
    """
    # TODO:
    # row = (
    #     db.get_db()
    #     .table("authorizations")
    #     .select("operations")
    #     .eq("userId", body.userId)
    #     .eq("module", body.owningModule)
    #     .maybe_single()
    #     .execute()
    # )
    # if not row.data:
    #     return {"authorized": False, "reason": "No authorization record found"}
    # authorized = body.operation in row.data["operations"]
    # return {"authorized": authorized}
    raise HTTPException(status_code=501, detail="Not implemented — awaiting Supabase tables")


# ---------------------------------------------------------------------------
# POST /auth/grant
# ---------------------------------------------------------------------------
@router.post("/grant", status_code=201)
async def grant_authorization(body: GrantAuthRequest):
    """
    Grants a user authorization for a module (and optionally specific operations).
    Placeholder — Supabase upsert will go here once tables are created.

    Upsert into authorizations, merging operations arrays if record exists.
    """
    # TODO:
    # db.get_db().table("authorizations").upsert({
    #     "userId": body.userId,
    #     "module": body.module,
    #     "operations": body.operations,
    #     "granted_by": body.grantedBy,
    #     "granted_at": "now()",
    # }).execute()
    return {
        "status": "granted",
        "userId": body.userId,
        "module": body.module,
        "operations": body.operations,
    }
