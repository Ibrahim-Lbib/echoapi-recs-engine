import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_get_recommendations(client):
    # Mock Redis to avoid connection issues during tests
    from unittest.mock import AsyncMock
    with patch("redis.asyncio.Redis") as mock_redis, \
         patch("app.services.api_key_service.ApiKeyService.validate_key", new_callable=AsyncMock) as mock_validate:
        mock_validate.return_value = True
        mock_instance = MagicMock()
        mock_instance.get = AsyncMock(return_value=None)  # Force DB fallback
        mock_instance.aclose = AsyncMock(return_value=None)
        mock_redis.return_value = mock_instance
        
        response = await client.get("/api/v1/recommend/?user_id=test_user_1", headers={"X-API-Key": "test_client_key"})
    
    assert response.status_code == 200
    assert "recommendations" in response.json()
