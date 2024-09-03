import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from user_manager.factory.database import Base, init_db
from user_manager.server import app
import os

DATABASE_URL = "sqlite+aiosqlite:///tests/test.db"


@pytest_asyncio.fixture(scope="function")
async def async_db() -> AsyncSession:
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        # Drop all tables
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncClient:
    await init_db()
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


def pytest_sessionfinish(session, exitstatus):
    try:
        os.remove('tests/test.db')
    except FileNotFoundError:
        pass
