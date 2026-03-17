from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class ItemBase(BaseModel):
    external_item_id: str
    metadata_json: Optional[Dict[str, Any]] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
