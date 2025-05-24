import pytest
import pytest_asyncio
from httpx import AsyncClient
from httpx import ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from main import app
from models import Base
import asyncio

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()

@pytest_asyncio.fixture(scope="session")
async def test_db():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    yield async_session
    await engine.dispose()

@pytest_asyncio.fixture
async def client(test_db):
    async def override_get_db():
        async with test_db() as session:
            yield session
    app.dependency_overrides = getattr(app, 'dependency_overrides', {})
    from database import get_db
    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_distance_success(client):
    payload = {
        "source": "415 Mission St, San Francisco, CA",
        "destination": "1600 Amphitheatre Parkway, Mountain View, CA"
    }
    response = await client.post("/distance", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "miles" in data and "kilometers" in data

@pytest.mark.asyncio
async def test_distance_invalid_address(client):
    payload = {
        "source": "123",
        "destination": "1600 Amphitheatre Parkway, Mountain View, CA"
    }
    response = await client.post("/distance", json=payload)
    assert response.status_code == 422  # Pydantic validation error

@pytest.mark.asyncio
async def test_history(client):
    # Should be empty or have one record if run after test_distance_success
    response = await client.get("/history")
    assert response.status_code == 200
    data = response.json()
    assert "history" in data 