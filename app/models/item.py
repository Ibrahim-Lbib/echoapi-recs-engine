from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    external_item_id = Column(String, unique=True, index=True, nullable=False)
    metadata_json = Column(JSON, nullable=True) # Renamed to avoid reserved keyword 'metadata'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
