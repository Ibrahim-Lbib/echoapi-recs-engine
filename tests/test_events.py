import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_track_event(client):
    response = await client.post(
        "/api/v1/events/track",
        json={
            "external_user_id": "test_user_1",
            "external_item_id": "test_item_1",
            "event_type": "view"
        }
    )
    assert response.status_code == 201
    assert response.json()["status"] == "success"
