import asyncio
from worker.background_tasks import train_model_task
from app.utils.logger import logger

async def start_scheduler():
    """
    Simple async scheduler for periodic tasks.
    In a real production app, this would be replaced by APScheduler or Celery Beat.
    """
    logger.info("Starting background scheduler...")
    while True:
        try:
            # Run training every 12 hours
            logger.info("Starting scheduled training job...")
            await train_model_task()
            logger.info("Scheduled training job completed. Sleeping for 12 hours.")
            await asyncio.sleep(43200) # 12 hours
        except Exception as e:
            logger.error(f"Scheduler error: {str(e)}")
            await asyncio.sleep(60) # Wait a bit before retrying on error

if __name__ == "__main__":
    asyncio.run(start_scheduler())
