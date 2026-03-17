from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.recommendation_cache import RecommendationCache
import redis.asyncio as redis
from app.core.config import settings
import json
from typing import List, Optional, Tuple

class CacheService:
    @staticmethod
    async def get_cached_recommendations(db: AsyncSession, user_id_internal: int, external_user_id: str) -> Tuple[Optional[List[str]], str]:
        r = redis.Redis(
            host=settings.REDIS_HOST, 
            port=settings.REDIS_PORT, 
            decode_responses=True,
            socket_timeout=2.0,
            socket_connect_timeout=2.0
        )
        try:
            cached = await r.get(f"recs:{external_user_id}")
            if cached:
                return json.loads(cached), "redis"
        except Exception:
            # Silent fail for redis in MVP
            pass
        finally:
            await r.aclose()

        # 2. Try DB
        stmt = select(RecommendationCache).where(RecommendationCache.user_id == user_id_internal)
        result = await db.execute(stmt)
        cache_entry = result.scalars().first()

        if cache_entry:
            return cache_entry.recommendations, "db"

        return None, "none"

    @staticmethod
    async def set_cached_recommendations(db: AsyncSession, user_id_internal: int, external_user_id: str, recommendations: List[str]):
        # 1. Update DB
        stmt = select(RecommendationCache).where(RecommendationCache.user_id == user_id_internal)
        result = await db.execute(stmt)
        cache_entry = result.scalars().first()

        if cache_entry:
            cache_entry.recommendations = recommendations
        else:
            cache_entry = RecommendationCache(user_id=user_id_internal, recommendations=recommendations)
            db.add(cache_entry)
        
        await db.commit()

        # 2. Update Redis
        r = redis.Redis(
            host=settings.REDIS_HOST, 
            port=settings.REDIS_PORT, 
            decode_responses=True,
            socket_timeout=2.0,
            socket_connect_timeout=2.0
        )
        try:
            await r.set(f"recs:{external_user_id}", json.dumps(recommendations), ex=3600) # 1 hour TTL
        except Exception:
            pass
        finally:
            await r.aclose()
