from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.dependencies import get_db
from app.core.config import settings
import redis.asyncio as redis

router = APIRouter()

@router.get("/")
async def health_check(db: AsyncSession = Depends(get_db)):
    health_status = {
        "status": "healthy",
        "components": {
            "api": "up",
            "database": "down",
            "redis": "down"
        }
    }
    
    # Check Database
    try:
        await db.execute(text("SELECT 1"))
        health_status["components"]["database"] = "up"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["components"]["database"] = f"error: {str(e)}"

    # Check Redis
    r = None
    try:
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
        await r.ping()
        health_status["components"]["redis"] = "up"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["components"]["redis"] = f"error: {str(e)}"
    finally:
        if r:
            await r.aclose()

    if health_status["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=health_status)
        
    return health_status
