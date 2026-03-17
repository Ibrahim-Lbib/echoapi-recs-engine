from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.recommendation_service import RecommendationService
from app.schemas.recommendation import RecommendationResponse

router = APIRouter()

@router.get("/", response_model=RecommendationResponse)
async def get_recommendations(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: str = Query(..., description="The external user ID")
):
    """
    Get personalized recommendations for a user.
    """
    recs, source, is_cold_start = await RecommendationService.get_recommendations(db, user_id)
    return RecommendationResponse(
        user_id=user_id, 
        recommendations=recs, 
        source=source, 
        cold_start=is_cold_start
    )
