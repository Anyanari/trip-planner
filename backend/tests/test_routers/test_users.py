import pytest
from fastapi.testclient import TestClient
from app.models import User


class TestUsersRouter:
    """Test cases for users router."""

    def test_create_user_success(self, client):
        """Test successful user creation."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser"
        }
        response = client.post("/api/users/", json=user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert "id" in data
        assert "created_time" in data

    def test_create_user_duplicate_email(self, client):
        """Test user creation with duplicate email."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser"
        }
        
        # Create first user
        response1 = client.post("/api/users/", json=user_data)
        assert response1.status_code == 200
        
        # Try to create second user with same email
        user_data2 = {
            "email": "test@example.com",
            "username": "testuser2"
        }
        response2 = client.post("/api/users/", json=user_data2)
        
        assert response2.status_code == 400
        assert "Email already registered" in response2.json()["detail"]

    def test_create_user_duplicate_username(self, client):
        """Test user creation with duplicate username."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser"
        }
        
        # Create first user
        response1 = client.post("/api/users/", json=user_data)
        assert response1.status_code == 200
        
        # Try to create second user with same username
        user_data2 = {
            "email": "test2@example.com",
            "username": "testuser"
        }
        response2 = client.post("/api/users/", json=user_data2)
        
        assert response2.status_code == 400
        assert "Username already taken" in response2.json()["detail"]

    def test_create_user_invalid_email(self, client):
        """Test user creation with invalid email."""
        user_data = {
            "email": "invalid-email",
            "username": "testuser"
        }
        response = client.post("/api/users/", json=user_data)
        
        assert response.status_code == 422  # Validation error

    def test_create_user_missing_fields(self, client):
        """Test user creation with missing required fields."""
        # Missing email
        user_data = {
            "username": "testuser"
        }
        response = client.post("/api/users/", json=user_data)
        assert response.status_code == 422

        # Missing username
        user_data = {
            "email": "test@example.com"
        }
        response = client.post("/api/users/", json=user_data)
        assert response.status_code == 422

    def test_get_users_empty(self, client):
        """Test getting users when database is empty."""
        response = client.get("/api/users/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_users_with_data(self, client):
        """Test getting users when database has data."""
        # Create some users
        users_data = [
            {"email": "user1@example.com", "username": "user1"},
            {"email": "user2@example.com", "username": "user2"},
            {"email": "user3@example.com", "username": "user3"}
        ]
        
        for user_data in users_data:
            client.post("/api/users/", json=user_data)
        
        response = client.get("/api/users/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
        
        # Check that all users are returned
        emails = [user["email"] for user in data]
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails
        assert "user3@example.com" in emails

    def test_get_users_with_pagination(self, client):
        """Test getting users with pagination parameters."""
        # Create some users
        users_data = [
            {"email": f"user{i}@example.com", "username": f"user{i}"}
            for i in range(5)
        ]
        
        for user_data in users_data:
            client.post("/api/users/", json=user_data)
        
        # Test with skip and limit
        response = client.get("/api/users/?skip=1&limit=2")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    def test_get_user_by_id_success(self, client):
        """Test getting a user by ID."""
        # Create a user
        user_data = {
            "email": "test@example.com",
            "username": "testuser"
        }
        create_response = client.post("/api/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Get the user
        response = client.get(f"/api/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]

    def test_get_user_by_id_not_found(self, client):
        """Test getting a non-existent user by ID."""
        response = client.get("/api/users/99999")
        
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    def test_get_user_by_id_invalid_id(self, client):
        """Test getting a user with invalid ID."""
        response = client.get("/api/users/invalid")
        
        assert response.status_code == 422  # Validation error

    def test_user_data_persistence(self, client, db_session):
        """Test that user data is properly persisted in database."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser"
        }
        
        # Create user via API
        response = client.post("/api/users/", json=user_data)
        assert response.status_code == 200
        
        # Check that user exists in database
        user_in_db = db_session.query(User).filter(
            User.email == user_data["email"]
        ).first()
        
        assert user_in_db is not None
        assert user_in_db.email == user_data["email"]
        assert user_in_db.username == user_data["username"]

    def test_user_response_model(self, client):
        """Test that user response matches the expected model."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser"
        }
        
        response = client.post("/api/users/", json=user_data)
        data = response.json()
        
        # Check required fields
        required_fields = ["id", "email", "username", "created_time"]
        for field in required_fields:
            assert field in data
        
        # Check that password is not in response (security)
        assert "password" not in data
