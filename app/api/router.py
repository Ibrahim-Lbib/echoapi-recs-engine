from fastapi import APIRouter
from app.api.routes import events, recommendations, training, health, keys

api_router = APIRouter()
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(recommendations.router, prefix="/recommend", tags=["recommendations"])
api_router.include_router(training.router, prefix="/train", tags=["training"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(keys.router, prefix="/keys", tags=["api-keys"])
