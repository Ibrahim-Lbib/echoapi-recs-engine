from pydantic import BaseModel, Field

class EventCreate(BaseModel):
    external_user_id: str
    external_item_id: str
    event_type: str = Field(..., description="view, click, or purchase")
