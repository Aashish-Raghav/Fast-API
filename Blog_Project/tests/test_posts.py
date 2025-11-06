"""
Tests for post endpoints (CRUD operations).
"""

import pytest
from httpx import AsyncClient
from app.models import User, Post


class TestPostEndpoints:
    """Test post-related endpoints."""

    @pytest.mark.asyncio
    async def test_create_post_success(
        self, client: AsyncClient, auth_headers: dict, test_user: User
    ):
        """Test creating a new post."""
        response = await client.post(
            "/posts/",
            headers=auth_headers,
            json={
                "title": "My First Post",
                "content": "This is the content of my first post.",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "My First Post"
        assert data["content"] == "This is the content of my first post."
        assert "id" in data
        assert "created_at" in data

    @pytest.mark.asyncio
    async def test_create_post_unauthorized(self, client: AsyncClient):
        """Test creating post without authentication."""
        response = await client.post(
            "/posts/",
            json={"title": "Unauthorized Post", "content": "This should fail."},
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_create_post_invalid_data(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test creating post with invalid data."""
        response = await client.post(
            "/posts/",
            headers=auth_headers,
            json={"title": "", "content": "Content here"},  # Empty title should fail
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_list_posts(self, client: AsyncClient, test_post: Post):
        """Test listing all posts (public endpoint)."""
        response = await client.get("/posts/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(post["id"] == test_post.id for post in data)

    @pytest.mark.asyncio
    async def test_get_post_by_id(self, client: AsyncClient, test_post: Post):
        """Test getting a specific post by ID."""
        response = await client.get(f"/posts/{test_post.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_post.id
        assert data["title"] == test_post.title
        assert data["content"] == test_post.content

    @pytest.mark.asyncio
    async def test_get_post_by_id_not_found(self, client: AsyncClient):
        """Test getting non-existent post."""
        response = await client.get("/posts/99999")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_posts_by_user(
        self, client: AsyncClient, test_user: User, test_post: Post
    ):
        """Test getting all posts by a specific user."""
        response = await client.get(f"/posts/user/{test_user.id}")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert all(
            post["id"] == test_post.id for post in data if post["id"] == test_post.id
        )

    @pytest.mark.asyncio
    async def test_get_posts_by_nonexistent_user(self, client: AsyncClient):
        """Test getting posts for non-existent user."""
        response = await client.get("/posts/user/99999")

        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_update_post_success(
        self, client: AsyncClient, auth_headers: dict, test_post: Post
    ):
        """Test updating own post."""
        response = await client.patch(
            f"/posts/{test_post.id}",
            headers=auth_headers,
            json={"title": "Updated Title", "content": "Updated content"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["content"] == "Updated content"
        assert data["id"] == test_post.id

    @pytest.mark.asyncio
    async def test_update_post_partial(
        self, client: AsyncClient, auth_headers: dict, test_post: Post
    ):
        """Test partially updating a post (only title)."""
        original_content = test_post.content
        response = await client.patch(
            f"/posts/{test_post.id}",
            headers=auth_headers,
            json={"title": "New Title Only"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title Only"
        assert data["content"] == original_content  # Content unchanged

    @pytest.mark.asyncio
    async def test_update_post_unauthorized(self, client: AsyncClient, test_post: Post):
        """Test updating post without authentication."""
        response = await client.patch(
            f"/posts/{test_post.id}", json={"title": "Hacked Title"}
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_update_other_users_post(
        self, client: AsyncClient, test_user_2: User, test_post: Post
    ):
        """Test that user cannot update another user's post."""
        # Login as test_user_2
        login_response = await client.post(
            "/auth/login", data={"username": "testuser2", "password": "password456"}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Try to update test_user's post
        response = await client.patch(
            f"/posts/{test_post.id}", headers=headers, json={"title": "Should Not Work"}
        )

        assert response.status_code == 404  # Post not found for this user

    @pytest.mark.asyncio
    async def test_update_nonexistent_post(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test updating non-existent post."""
        response = await client.patch(
            "/posts/99999", headers=auth_headers, json={"title": "New Title"}
        )

        assert response.status_code == 404
