import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from user_schema.schemas import UserCreate, UserUpdate
from your_module import (
    create_user, get_user, get_users,
    update_user, delete_user
)
from db_model.base import Base

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# Setup test database and session fixture
@pytest.fixture(scope='function')
async def async_db():
    # Create a new async engine for the SQLite memory database
    engine = create_async_engine(DATABASE_URL, echo=False, poolclass=NullPool)

    # Create tables in the test database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create a new session for each test
    async_session = sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession
    )

    async with async_session() as session:
        yield session

    # Drop tables after tests
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.mark.asyncio
async def test_create_user(async_db):
    user_data = UserCreate(
        username="testuser",
        email="testuser@example.com",
        password="password123"
    )
    created_user = await create_user(async_db, user_data)

    assert created_user.id is not None
    assert created_user.username == user_data.username
    assert created_user.email == user_data.email


@pytest.mark.asyncio
async def test_get_user(async_db):
    # Create a user first
    user_data = UserCreate(
        username="testuser",
        email="testuser@example.com",
        password="password123"
    )
    created_user = await create_user(async_db, user_data)

    # Now fetch the user by id
    fetched_user = await get_user(async_db, created_user.id)

    assert fetched_user is not None
    assert fetched_user.id == created_user.id
    assert fetched_user.username == created_user.username


@pytest.mark.asyncio
async def test_get_users(async_db):
    # Create multiple users
    user_data_1 = UserCreate(
        username="user1",
        email="user1@example.com",
        password="password123"
    )
    user_data_2 = UserCreate(
        username="user2",
        email="user2@example.com",
        password="password123"
    )
    await create_user(async_db, user_data_1)
    await create_user(async_db, user_data_2)

    # Get all users with limit
    users = await get_users(async_db, skip=0, limit=10)

    assert len(users) == 2


@pytest.mark.asyncio
async def test_update_user(async_db):
    # Create a user first
    user_data = UserCreate(
        username="testuser",
        email="testuser@example.com",
        password="password123"
    )
    created_user = await create_user(async_db, user_data)

    # Update the user
    update_data = UserUpdate(
        username="updateduser",
        email="updated@example.com"
    )
    updated_user = await update_user(async_db, created_user.id, update_data)

    assert updated_user.username == "updateduser"
    assert updated_user.email == "updated@example.com"


@pytest.mark.asyncio
async def test_delete_user(async_db):
    # Create a user first
    user_data = UserCreate(
        username="testuser",
        email="testuser@example.com",
        password="password123"
    )
    created_user = await create_user(async_db, user_data)

    # Delete the user
    deleted_user = await delete_user(async_db, created_user.id)

    assert deleted_user is not None

    # Verify the user was deleted
    fetched_user = await get_user(async_db, created_user.id)
    assert fetched_user is None
