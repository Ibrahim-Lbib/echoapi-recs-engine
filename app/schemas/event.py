from pydantic import BaseModel
from typing import Literal

class EventCreate(BaseModel):
    external_user_id: str
    external_item_id: str
    event_type: Literal["view", "click", "purchase"]
