from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional
from app.core.dependencies import verify_api_key
from app.services.api_key_service import ApiKeyService
from app.core.supabase import get_supabase

router = APIRouter()

async def get_user_from_token(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    token = authorization.split(" ")[1]
    supabase = get_supabase()
    try:
        user = supabase.auth.get_user(token)
        return user.user.id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.post("/generate", status_code=201)
async def generate_key(
    label: str = "default",
    user_id: str = Depends(get_user_from_token)
):
    raw_key = await ApiKeyService.generate_key(user_id=user_id, label=label)
    return {
        "api_key": raw_key,
        "message": "Store this key securely — it will not be shown again."
    }

@router.get("/list")
async def list_keys(user_id: str = Depends(get_user_from_token)):
    keys = await ApiKeyService.list_keys(user_id)
    return {"keys": keys}

@router.delete("/revoke/{prefix}")
async def revoke_key(prefix: str, user_id: str = Depends(get_user_from_token)):
    success = await ApiKeyService.revoke_key(prefix, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"status": "revoked", "prefix": prefix}
