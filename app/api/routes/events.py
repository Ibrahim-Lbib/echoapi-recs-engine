from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import verify_client_api_key
from app.schemas.event import EventCreate
from app.services.event_service import EventService

router = APIRouter()

@router.post("/track", status_code=201, dependencies=[Depends(verify_client_api_key)])
async def track_event(
    *,
    db: AsyncSession = Depends(get_db),
    event_in: EventCreate
):
    """
    Track a user event (view, click, purchase).
    """
    event = await EventService.track_event(db, event_in)
    return {"status": "success", "event_id": event.id}
