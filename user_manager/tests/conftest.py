from server import app
from factory.database import SessionLocal, engine, Base
import pytest
from httpx import AsyncClient


@pytest.fixture(scope="module")
async def db():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield SessionLocal

    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_session():
    async with SessionLocal() as session:  # Replace with actual session setup
        yield session


@pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
