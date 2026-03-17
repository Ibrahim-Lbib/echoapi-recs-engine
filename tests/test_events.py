import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_track_event(client):
    with patch("app.services.api_key_service.ApiKeyService.validate_key", new_callable=AsyncMock) as mock_validate:
        mock_validate.return_value = True
        response = await client.post(
            "/api/v1/events/track",
            json={
                "external_user_id": "test_user_1",
                "external_item_id": "test_item_1",
                "event_type": "view"
            },
            headers={"X-API-Key": "test_client_key"}
        )
    assert response.status_code == 201
    assert response.json()["status"] == "success"
