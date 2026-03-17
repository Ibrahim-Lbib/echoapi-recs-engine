import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

from app.core.config import settings

@pytest.mark.asyncio
async def test_train_model_unauthorized(client):
    response = await client.post("/api/v1/train/")
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_train_model_authorized(client):
    headers = {"X-API-Key": settings.API_KEY}
    response = await client.post("/api/v1/train/", headers=headers)
    # Since we might not have data, it could return 202
    assert response.status_code == 202
