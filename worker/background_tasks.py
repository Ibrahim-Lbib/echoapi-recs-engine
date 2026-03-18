from app.services.training_service import TrainingService
from app.db.session import SessionLocal
from app.utils.logger import logger

async def train_model_task():
    """
    Background task to trigger model training.
    """
    logger.info("Executing background training task...")
    async with SessionLocal() as db:
        result = await TrainingService.run_training(db)
        logger.info(f"Background training result: {result}")
    return result
