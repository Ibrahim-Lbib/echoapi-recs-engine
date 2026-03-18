import os
os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["API_KEY"] = "test_admin_key"
os.environ["SUPABASE_URL"] = "https://test.supabase.co"
os.environ["SUPABASE_SERVICE_KEY"] = "test_service_key"

import asyncio
import sys

import pytest
from httpx import AsyncClient, ASGITransport

from app.db import session as db_session
from app.main import app

def pytest_configure(config):
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def cleanup_db(event_loop):
    # The engine will be lazily initialized in app.db.session.get_db
    yield
    if db_session.engine:
        await db_session.engine.dispose()

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
