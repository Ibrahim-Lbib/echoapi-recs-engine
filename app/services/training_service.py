from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.ml.trainer import Trainer
from app.services.cache_service import CacheService
import logging

logger = logging.getLogger(__name__)

class TrainingService:
    @staticmethod
    async def run_training(db: AsyncSession):
        """
        Orchestrates the training process:
        1. Run Trainer logic to get new recommendations.
        2. Fetch external IDs for users to update Redis.
        3. Update CacheService with the results.
        """
        logger.info("Starting training process...")
        try:
            # 1. Run trainer (returns {internal_user_id: [external_item_ids]})
            recommendations_map = await Trainer.train_v1(db)
            
            if not recommendations_map:
                return {"status": "success", "message": "No data to train on"}

            # 2. Fetch user mapping for Redis (internal_id -> external_id)
            stmt_users = select(User).where(User.id.in_(list(recommendations_map.keys())))
            res_users = await db.execute(stmt_users)
            user_mapping = {u.id: u.external_user_id for u in res_users.scalars().all()}

            # 3. Update cache for each user
            for user_internal_id, recs in recommendations_map.items():
                external_user_id = user_mapping.get(user_internal_id)
                if external_user_id:
                    await CacheService.set_cached_recommendations(
                        db, 
                        user_id_internal=user_internal_id, 
                        external_user_id=external_user_id, 
                        recommendations=recs
                    )

            logger.info(f"Training process completed. Processed {len(recommendations_map)} users.")
            return {"status": "success", "message": f"Model trained and cache updated for {len(recommendations_map)} users"}
        except Exception as e:
            logger.error(f"Training failed: {str(e)}")
            return {"status": "error", "message": str(e)}
