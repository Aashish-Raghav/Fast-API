"""
Integration tests for complete workflows.
"""
import pytest
from httpx import AsyncClient
from app.models import Post


class TestIntegrationWorkflows:
    """Test complete user workflows."""

    @pytest.mark.asyncio
    async def test_complete_user_workflow(self, client: AsyncClient):
        """
        Test complete workflow: register → login → create post → read post → update post.
        """
        # 1. Register a new user
        register_response = await client.post(
            "/auth/register",
            json={
                "fullname": "Workflow User",
                "username": "workflowuser",
                "email": "workflow@example.com",
                "password": "workflow123"
            }
        )
        assert register_response.status_code == 201
        user_id = register_response.json()["id"]
        
        # 2. Login
        login_response = await client.post(
            "/auth/login",
            data={
                "username": "workflowuser",
                "password": "workflow123"
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Get current user info
        me_response = await client.get("/users/me", headers=headers)
        assert me_response.status_code == 200
        assert me_response.json()["email"] == "workflow@example.com"
        
        # 4. Create a post
        post_response = await client.post(
            "/posts/",
            headers=headers,
            json={
                "title": "Integration Test Post",
                "content": "This is an integration test."
            }
        )
        assert post_response.status_code == 201
        post_id = post_response.json()["id"]
        
        # 5. Read the post
        get_post_response = await client.get(f"/posts/{post_id}")
        assert get_post_response.status_code == 200
        assert get_post_response.json()["title"] == "Integration Test Post"
        
        # 6. Update the post
        update_response = await client.patch(
            f"/posts/{post_id}",
            headers=headers,
            json={"title": "Updated Integration Post"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["title"] == "Updated Integration Post"
        
        # 7. Get user's posts
        user_posts_response = await client.get(f"/posts/user/{user_id}")
        assert user_posts_response.status_code == 200
        assert len(user_posts_response.json()) >= 1

    @pytest.mark.asyncio
    async def test_unauthorized_access_workflow(self, client: AsyncClient, test_post: Post):
        """Test that unauthorized users cannot access protected endpoints."""
        # Try to create post without auth
        create_response = await client.post(
            "/posts/",
            json={"title": "No Auth", "content": "Should fail"}
        )
        assert create_response.status_code == 401
        
        # Try to access /users/me without auth
        me_response = await client.get("/users/me")
        assert me_response.status_code == 401
        
        # Try to update post without auth
        update_response = await client.patch(
            f"/posts/{test_post.id}",
            json={"title": "Hacked"}
        )
        assert update_response.status_code == 401
        
        # Public endpoints should work
        list_posts = await client.get("/posts/")
        assert list_posts.status_code == 200

        get_post = await client.get(f"/posts/{test_post.id}")
        assert get_post.status_code == 200
