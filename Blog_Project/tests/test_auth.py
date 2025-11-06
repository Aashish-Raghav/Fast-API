"""
Tests for authentication endpoints (register, login).
"""

import pytest
from httpx import AsyncClient
from app.models import User


class TestAuthEndpoints:
    """Test Authentication related testpoints"""

    @pytest.mark.asyncio
    async def test_register_success(self, client: AsyncClient):
        response = await client.post(
            "/auth/register",
            json={
                "fullname": "New User",
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "securepass123",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert "id" in data
        assert "hashed_password" not in data

    @pytest.mark.asyncio
    async def test_register_duplicate(self, client: AsyncClient, test_user: User):
        response = await client.post(
            "/auth/register",
            json={
                "fullname": "New User",
                "username": "testuser",
                "email": "newuser@example.com",
                "password": "securepass123",
            },
        )

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_invalid_email(self, client: AsyncClient):
        response = await client.post(
            "/auth/register",
            json={
                "fullname": "New User",
                "username": "testuser",
                "email": "wrong-email",
            },
        )

        assert response.status_code == 422  # validation erro

    @pytest.mark.asyncio
    async def test_register_short_password(self, client: AsyncClient):
        """Test registration with password too short."""
        response = await client.post(
            "/auth/register",
            json={
                "username": "user",
                "email": "user@example.com",
                "password": "123",  # Too short
            },
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_login(self, client: AsyncClient, test_user: User):
        response = await client.post(
            "/auth/login", data={"username": "testuser", "password": "testpassword123"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client: AsyncClient, test_user: User):
        response = await client.post(
            "/auth/login", data={"username": "testuser", "password": "wrong-password"}
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client: AsyncClient):
        response = await client.post(
            "/auth/login", data={"username": "testuser", "password": "testpassword123"}
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_missing_credentials(self, client: AsyncClient):
        response = await client.post("/auth/login", data={})

        assert response.status_code == 422
