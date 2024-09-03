import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    user_data = {
        "username": "johndoe",
        "email": "john@example.com",
        "full_name": "John Doe",
    }
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "johndoe"
    assert data["email"] == "john@example.com"
    assert data["full_name"] == "John Doe"

    # Delete the user
    response = await client.delete(f"/users/{data['id']}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_read_user(client: AsyncClient):
    # Create a user first
    user_data = {
        "username": "johndoe",
        "email": "john@example.com",
        "full_name": "John Doe",
    }
    response = await client.get("/users/1")
    assert response.status_code == 404

    create_response = await client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]

    # Read the created user
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "johndoe"
    assert data["email"] == "john@example.com"
    assert data["full_name"] == "John Doe"

    # Delete the user
    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient):
    # Create a user first
    user_data = {
        "username": "johndoe",
        "email": "john@example.com",
        "full_name": "John Doe",
    }
    create_response = await client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]

    # Update the user
    updated_data = {
        "username": "johnsmith",
        "email": "johnsmith@example.com",
        "full_name": "John Smith",
    }
    response = await client.put(f"/users/{user_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "johnsmith"
    assert data["email"] == "johnsmith@example.com"
    assert data["full_name"] == "John Smith"

    # Delete the user
    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    # Create a user first
    user_data = {
        "username": "johndoe",
        "email": "john@example.com",
        "full_name": "John Doe",
    }
    create_response = await client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]

    # Delete the user
    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 200

    # Try to read the deleted user
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 404

    # Try to delete the user again
    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 404
