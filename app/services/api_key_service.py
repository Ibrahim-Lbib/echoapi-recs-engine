import secrets
import hashlib
from app.core.supabase import get_supabase

class ApiKeyService:

    @staticmethod
    def _hash_key(raw_key: str) -> str:
        return hashlib.sha256(raw_key.encode()).hexdigest()

    @staticmethod
    async def generate_key(user_id: str, label: str = "default") -> str:
        supabase = get_supabase()
        raw_key = f"echo_{secrets.token_urlsafe(32)}"
        key_hash = ApiKeyService._hash_key(raw_key)
        prefix = raw_key[:12]
        supabase.table("api_keys").insert({
            "user_id": user_id,
            "key_hash": key_hash,
            "key_prefix": prefix,
            "label": label,
            "is_active": True
        }).execute()
        return raw_key

    @staticmethod
    async def validate_key(raw_key: str) -> bool:
        supabase = get_supabase()
        key_hash = ApiKeyService._hash_key(raw_key)
        result = supabase.table("api_keys").select("id, is_active").eq(
            "key_hash", key_hash
        ).single().execute()
        if not result.data or not result.data.get("is_active"):
            return False
        supabase.table("api_keys").update(
            {"last_used_at": "now()"}
        ).eq("key_hash", key_hash).execute()
        return True

    @staticmethod
    async def revoke_key(key_prefix: str, user_id: str) -> bool:
        supabase = get_supabase()
        result = supabase.table("api_keys").update(
            {"is_active": False}
        ).eq("key_prefix", key_prefix).eq("user_id", user_id).execute()
        return bool(result.data)

    @staticmethod
    async def list_keys(user_id: str) -> list:
        supabase = get_supabase()
        result = supabase.table("api_keys").select(
            "key_prefix, label, is_active, created_at, last_used_at"
        ).eq("user_id", user_id).execute()
        return result.data or []
