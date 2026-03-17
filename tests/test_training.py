import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_train_model(client):
    response = await client.post("/api/v1/train/")
    # Since we might not have data, it could return 202 and "No data to train on"
    assert response.status_code == 202
