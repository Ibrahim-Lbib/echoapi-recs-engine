from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.models.item import Item
from app.models.event import Event
from app.schemas.event import EventCreate

class EventService:
    @staticmethod
    async def track_event(db: AsyncSession, event_in: EventCreate):
        # 1. Ensure user exists
        stmt = select(User).where(User.external_user_id == event_in.external_user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()
        if not user:
            user = User(external_user_id=event_in.external_user_id)
            db.add(user)
            await db.flush()

        # 2. Ensure item exists
        stmt = select(Item).where(Item.external_item_id == event_in.external_item_id)
        result = await db.execute(stmt)
        item = result.scalars().first()
        if not item:
            item = Item(external_item_id=event_in.external_item_id)
            db.add(item)
            await db.flush()

        # 3. Save event
        db_event = Event(
            user_id=user.id,
            item_id=item.id,
            event_type=event_in.event_type
        )
        db.add(db_event)
        await db.commit()
        return db_event
