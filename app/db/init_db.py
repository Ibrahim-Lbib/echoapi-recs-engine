import asyncio
from app.db.session import engine
from app.db.base import Base
from app.models.user import User
from app.models.item import Item
from app.models.event import Event
from app.models.recommendation_cache import RecommendationCache

async def init_models():
    async with engine.begin() as conn:
        # For development, we can drop and recreate
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully.")

if __name__ == "__main__":
    asyncio.run(init_models())
