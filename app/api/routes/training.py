from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, SessionLocal, verify_api_key
from app.services.training_service import TrainingService

router = APIRouter()

async def run_training_wrapper():
    """Wrapper to handle DB session for background task"""
    async with SessionLocal() as db:
        await TrainingService.run_training(db)

@router.post("/", status_code=202, dependencies=[Depends(verify_api_key)])
async def train_model(
    background_tasks: BackgroundTasks
):
    """
    Trigger training of the recommendation model.
    Returns immediately, training continues in background.
    """
    background_tasks.add_task(run_training_wrapper)
    return {"status": "success", "message": "Training started in background"}
