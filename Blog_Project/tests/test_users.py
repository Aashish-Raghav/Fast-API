"""
Tests for user endpoints (/users/me, /users, /users/{id}).
"""

import pytest
from httpx import AsyncClient
from app.models import User


class TestUserEndpoints:
    """Test user-related endpoints."""

    @pytest.mark.asyncio
    async def test_read_current_user_success(
        self, client: AsyncClient, auth_headers: dict, test_user: User
    ):
        """Test getting current user information."""
        response = await client.get("/users/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["username"] == test_user.username
        assert data["id"] == test_user.id

    @pytest.mark.asyncio
    async def test_read_current_user_unauthorized(self, client: AsyncClient):
        """Test accessing /users/me without authentication."""
        response = await client.get("/users/me")

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_read_current_user_invalid_token(self, client: AsyncClient):
        """Test accessing /users/me with invalid token."""
        response = await client.get(
            "/users/me", headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_list_users(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_user: User,
        test_user_2: User,
    ):
        """Test listing all users."""
        response = await client.get("/users/", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2
        emails = [user["email"] for user in data]
        assert test_user.email in emails
        assert test_user_2.email in emails

    @pytest.mark.asyncio
    async def test_list_users_unauthorized(self, client: AsyncClient):
        """Test listing users without authentication."""
        response = await client.get("/users/")

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_user_by_id(
        self, client: AsyncClient, auth_headers: dict, test_user: User
    ):
        """Test getting a specific user by ID."""
        response = await client.get(f"/users/{test_user.id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["email"] == test_user.email

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test getting non-existent user."""
        response = await client.get("/users/99999", headers=auth_headers)

        assert response.status_code == 404
