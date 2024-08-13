import pytest
from httpx import AsyncClient
from user_manager.server import app
from user_manager.factory.database import SessionLocal, engine, Base


@pytest.fixture(scope="module")
async def db():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield SessionLocal

    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
