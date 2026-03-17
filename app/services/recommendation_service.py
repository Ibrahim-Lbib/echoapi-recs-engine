from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, case
from app.models.user import User
from app.models.event import Event
from app.models.item import Item
from app.services.cache_service import CacheService

class RecommendationService:
    @staticmethod
    async def get_popular_items(db: AsyncSession, limit: int = 10):
        """
        Query top items based on weighted interaction scores:
        Purchase: 3, Click: 2, View: 1
        """
        # Define weights
        purchase_weight = case((Event.event_type == 'purchase', 3), else_=0)
        click_weight = case((Event.event_type == 'click', 2), else_=0)
        view_weight = case((Event.event_type == 'view', 1), else_=0)
        
        total_weight = purchase_weight + click_weight + view_weight
        
        stmt = (
            select(Item.external_item_id)
            .join(Event, Event.item_id == Item.id)
            .group_by(Item.external_item_id)
            .order_by(func.sum(total_weight).desc())
            .limit(limit)
        )
        
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_recommendations(db: AsyncSession, external_user_id: str):
        # 1. Get internal user
        stmt = select(User).where(User.external_user_id == external_user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()
        
        # 2. Check if user is a cold start (no user model or no interactions)
        is_cold_start = False
        if not user:
            is_cold_start = True
        else:
            # Check for any interactions (even a quick count)
            event_stmt = select(func.count(Event.id)).where(Event.user_id == user.id)
            event_res = await db.execute(event_stmt)
            if event_res.scalar() == 0:
                is_cold_start = True

        if is_cold_start:
            popular_items = await RecommendationService.get_popular_items(db)
            return popular_items, "popular", True

        # 3. Check Cache for existing users
        recs, source = await CacheService.get_cached_recommendations(db, user.id, external_user_id)
        if recs:
            return recs, source, False

        # 4. Fallback: popular items instead of empty
        popular_items = await RecommendationService.get_popular_items(db)
        return popular_items, "popular_fallback", True
