import pytest
from user_schema.schemas import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from user_manager.api.crud import (
    create_user, get_user, get_users,
    update_user, delete_user
)  # Update import paths accordingly


@pytest.mark.asyncio
async def test_create_user(async_session: AsyncSession):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com"
    )
    db_user = await create_user(async_session, user_data)
    assert db_user.id is not None
    assert db_user.username == "testuser"
    assert db_user.email == "test@example.com"


@pytest.mark.asyncio
async def test_get_user(async_session: AsyncSession):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com"
    )
    db_user = await create_user(async_session, user_data)
    found_user = await get_user(async_session, db_user.id)
    assert found_user is not None
    assert found_user.id == db_user.id


@pytest.mark.asyncio
async def test_get_users(async_session: AsyncSession):
    user_data1 = UserCreate(
        username="testuser1",
        email="test1@example.com"
    )
    user_data2 = UserCreate(
        username="testuser2",
        email="test2@example.com"
    )
    await create_user(async_session, user_data1)
    await create_user(async_session, user_data2)

    users = await get_users(async_session, skip=0, limit=10)
    assert len(users) == 2


@pytest.mark.asyncio
async def test_update_user(async_session: AsyncSession):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com"
    )
    db_user = await create_user(async_session, user_data)

    update_data = UserUpdate(
        username="updateduser",
        email="updated@example.com"
    )
    updated_user = await update_user(
        async_session, db_user.id, update_data
    )

    assert updated_user.username == "updateduser"
    assert updated_user.email == "updated@example.com"


@pytest.mark.asyncio
async def test_delete_user(async_session: AsyncSession):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com"
    )
    db_user = await create_user(async_session, user_data)

    deleted_user = await delete_user(async_session, db_user.id)
    assert deleted_user is not None

    found_user = await get_user(async_session, db_user.id)
    assert found_user is None
