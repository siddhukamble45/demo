import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from user_manager.api.crud import (
    create_user, get_user, get_users,
    update_user, delete_user)  # Adjust import paths
from user_manager.user_schema.schemas import UserCreate, UserUpdate


class TestsUserCRUD:
    @pytest.mark.asyncio
    async def test_create_user(self, async_db: AsyncSession):
        user_data = UserCreate(
            username="testuser",
            email="testuser@example.com",
            full_name="Test User"
        )
        created_user = await create_user(async_db, user_data)

        assert created_user.id is not None
        assert created_user.username == user_data.username
        assert created_user.email == user_data.email
        assert created_user.full_name == "Test User"

    @pytest.mark.asyncio
    async def test_get_user(self, async_db: AsyncSession):
        user_data = UserCreate(
            username="testuser",
            email="testuser@example.com",
            full_name="Test User"
        )
        created_user = await create_user(async_db, user_data)
        fetched_user = await get_user(async_db, created_user.id)

        assert fetched_user is not None
        assert fetched_user.id == created_user.id
        assert fetched_user.username == created_user.username

        # Test for a non-existent user
        non_existent_user = await get_user(async_db, 9999)
        assert non_existent_user is None

    @pytest.mark.asyncio
    async def test_get_users(self, async_db: AsyncSession):
        user_data_1 = UserCreate(
            username="testuser_1",
            email="testuser@example.com",
            full_name="Test User"
        )
        user_data_2 = UserCreate(
            username="testuser_2",
            email="testuser@example.com",
            full_name="Test User"
        )
        await create_user(async_db, user_data_1)
        await create_user(async_db, user_data_2)

        users = await get_users(async_db, skip=0, limit=10)
        assert len(users) == 2

        # Test pagination
        users = await get_users(async_db, skip=1, limit=10)
        assert len(users) == 1
        assert users[0].username == "testuser_2"

    @pytest.mark.asyncio
    async def test_update_user(self, async_db: AsyncSession):
        user_data = UserCreate(
            username="testuser",
            email="testuser@example.com",
            full_name="Test User"
        )
        created_user = await create_user(async_db, user_data)

        update_data = UserUpdate(
            username="updateduser",
            email="updated@example.com",
            full_name="Updated Name"
        )
        updated_user = await update_user(
            async_db,
            created_user.id,
            update_data
        )

        assert updated_user is not None
        assert updated_user.username == "updateduser"
        assert updated_user.email == "updated@example.com"
        assert updated_user.full_name == "Updated Name"

        # Test updating a non-existent user
        non_existent_user_id = 9999
        non_existent_update_data = UserUpdate(
            username="newusername",
            email="newemail@example.com",
            full_name="Updated Name"
        )
        result = await update_user(
            async_db,
            non_existent_user_id,
            non_existent_update_data
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_delete_user(self, async_db: AsyncSession):
        user_data = UserCreate(
            username="testuser",
            email="testuser@example.com",
            full_name="Test User"
        )
        created_user = await create_user(async_db, user_data)

        deleted_user = await delete_user(async_db, created_user.id)
        assert deleted_user is not None

        # Verify the user was deleted
        fetched_user = await get_user(async_db, created_user.id)
        assert fetched_user is None

        # Test deleting a non-existent user
        non_existent_user_id = 9999
        result = await delete_user(async_db, non_existent_user_id)
        assert result is None
