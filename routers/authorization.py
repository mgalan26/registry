from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import json

from db import get_db

router = APIRouter()


class CheckAuthRequest(BaseModel):
    requestingModule: str
    owningModule: str
    userId: str
    operation: str


class GrantAuthRequest(BaseModel):
    userId: str
    moduloSolicitante: str
    moduloPropietario: str
    alcance: list[str] = []
    grantedBy: Optional[str] = None


# ---------------------------------------------------------------------------
# POST /auth/grant
# ---------------------------------------------------------------------------
@router.post("/grant", status_code=201)
async def grant_authorization(body: GrantAuthRequest):
    try:
        db = get_db()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"DB init error: {e}")

    try:
        db.table("autorizaciones_usuario").upsert(
            {
                "usuario_id": body.userId,
                "modulo_solicitante": body.moduloSolicitante,
                "modulo_propietario": body.moduloPropietario,
                "alcance": json.dumps(body.alcance),
                "activa": True,
            },
            on_conflict="usuario_id,modulo_solicitante,modulo_propietario",
        ).execute()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"grant error: {e}")

    return {
        "status": "granted",
        "userId": body.userId,
        "moduloSolicitante": body.moduloSolicitante,
        "moduloPropietario": body.moduloPropietario,
        "alcance": body.alcance,
    }


# ---------------------------------------------------------------------------
# POST /auth/check
# ---------------------------------------------------------------------------
@router.post("/check")
async def check_authorization(body: CheckAuthRequest):
    try:
        db = get_db()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"DB init error: {e}")

    try:
        result = (
            db.table("autorizaciones_usuario")
            .select("alcance")
            .eq("usuario_id", body.userId)
            .eq("modulo_solicitante", body.requestingModule)
            .eq("modulo_propietario", body.owningModule)
            .eq("activa", True)
            .maybe_single()
            .execute()
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"check error: {e}")

    if not result.data:
        return {"authorized": False, "reason": "No authorization record found"}

    alcance = result.data["alcance"]
    if isinstance(alcance, str):
        alcance = json.loads(alcance)

    authorized = body.operation in alcance
    return {"authorized": authorized}
