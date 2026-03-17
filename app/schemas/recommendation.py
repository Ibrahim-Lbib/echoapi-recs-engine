from pydantic import BaseModel, Field
from typing import List

class RecommendationResponse(BaseModel):
    user_id: str
    recommendations: List[str]
    source: str = Field(..., description="cache or fresh")
    cold_start: bool = False
