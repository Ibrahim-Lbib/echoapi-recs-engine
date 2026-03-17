from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.services.cache_service import CacheService

class RecommendationService:
    @staticmethod
    async def get_recommendations(db: AsyncSession, external_user_id: str):
        # 1. Get internal user
        stmt = select(User).where(User.external_user_id == external_user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()
        if not user:
            return [], "none"

        # 2. Check Cache
        recs, source = await CacheService.get_cached_recommendations(db, user.id, external_user_id)
        if recs:
            return recs, source

        # 3. Fallback: Fresh calculation (If no cache, return empty for now)
        # In a real app, you might trigger a fresh calc if cache is empty
        return [], "none"
