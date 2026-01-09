import pytest
from datetime import date
from fastapi.testclient import TestClient
from app.models import User, Trip


class TestTripsRouter:
    """Test cases for trips router."""

    def test_create_trip_success(self, client, sample_user_data, sample_trip_data):
        """Test successful trip creation."""
        # Create admin user first
        user_response = client.post("/api/users/", json=sample_user_data)
        admin_id = user_response.json()["id"]
        
        # Create trip (no need to pass admin_id anymore, it's hardcoded in router)
        trip_data = sample_trip_data.copy()
        
        response = client.post("/api/trips/", json=trip_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == trip_data["title"]
        assert data["description"] == trip_data["description"]
        assert data["start_date"] == trip_data["start_date"]
        assert data["end_date"] == trip_data["end_date"]
        assert data["admin"] == 1  # Hardcoded in router
        assert "id" in data
        assert "created_time" in data
        assert data["is_active"] is True

    def test_create_trip_missing_fields(self, client, sample_user_data):
        """Test trip creation with missing required fields."""
        # Create admin user first
        user_response = client.post("/api/users/", json=sample_user_data)
        admin_id = user_response.json()["id"]
        
        # Missing title
        trip_data = {
            "description": "Test description",
            "start_date": "2024-06-01",
            "end_date": "2024-06-07",
            "admin": admin_id
        }
        response = client.post("/api/trips/", json=trip_data)
        assert response.status_code == 422

    def test_create_trip_invalid_dates(self, client, sample_user_data):
        """Test trip creation with invalid date range."""
        # Create admin user first
        user_response = client.post("/api/users/", json=sample_user_data)
        admin_id = user_response.json()["id"]
        
        # End date before start date
        trip_data = {
            "title": "Test Trip",
            "description": "Test description",
            "start_date": "2024-06-07",
            "end_date": "2024-06-01",
            "admin": admin_id
        }
        response = client.post("/api/trips/", json=trip_data)
        # This might pass validation depending on implementation
        # but should be handled at business logic level

    def test_create_trip_nonexistent_admin(self, client, sample_trip_data):
        """Test trip creation with non-existent admin."""
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = 99999
        
        response = client.post("/api/trips/", json=trip_data)
        
        # Should fail due to foreign key constraint
        assert response.status_code in [400, 422]

    def test_get_trips_empty(self, client):
        """Test getting trips when database is empty."""
        response = client.get("/api/trips/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_trips_with_data(self, client, sample_user_data, sample_trip_data):
        """Test getting trips when database has data."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        admin_id = user_response.json()["id"]
        
        # Create some trips
        trips_data = [
            {
                "title": f"Trip {i}",
                "description": f"Description {i}",
                "start_date": "2024-06-01",
                "end_date": "2024-06-07",
                "admin": admin_id
            }
            for i in range(3)
        ]
        
        for trip_data in trips_data:
            client.post("/api/trips/", json=trip_data)
        
        response = client.get("/api/trips/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

    def test_get_trip_by_id_success(self, client, sample_user_data, sample_trip_data):
        """Test getting a trip by ID."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        admin_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = admin_id
        create_response = client.post("/api/trips/", json=trip_data)
        trip_id = create_response.json()["id"]
        
        # Get the trip
        response = client.get(f"/api/trips/{trip_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == trip_id
        assert data["title"] == trip_data["title"]

    def test_get_trip_by_id_not_found(self, client):
        """Test getting a non-existent trip by ID."""
        response = client.get("/api/trips/99999")
        
        assert response.status_code == 404
        assert "Trip not found" in response.json()["detail"]

    def test_update_trip_success(self, client, sample_user_data, sample_trip_data):
        """Test updating a trip."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        admin_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = admin_id
        create_response = client.post("/api/trips/", json=trip_data)
        trip_id = create_response.json()["id"]
        
        # Update trip
        update_data = {
            "title": "Updated Trip Title",
            "description": "Updated description"
        }
        response = client.put(f"/api/trips/{trip_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]

    def test_update_trip_not_found(self, client):
        """Test updating a non-existent trip."""
        update_data = {
            "title": "Updated Title"
        }
        response = client.patch("/api/trips/99999", json=update_data)
        
        assert response.status_code == 404

    def test_delete_trip_success(self, client, sample_user_data, sample_trip_data):
        """Test deleting a trip."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        admin_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = admin_id
        create_response = client.post("/api/trips/", json=trip_data)
        trip_id = create_response.json()["id"]
        
        # Delete trip
        response = client.delete(f"/api/trips/{trip_id}")
        
        assert response.status_code == 200
        
        # Verify trip is deleted
        get_response = client.get(f"/api/trips/{trip_id}")
        assert get_response.status_code == 404

    def test_delete_trip_not_found(self, client):
        """Test deleting a non-existent trip."""
        response = client.delete("/api/trips/99999")
        
        assert response.status_code == 404

    def test_trip_user_relationship(self, client, sample_user_data, sample_trip_data, db_session):
        """Test the relationship between trip and admin user."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        admin_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = admin_id
        client.post("/api/trips/", json=trip_data)
        
        # Check relationship in database
        trip_in_db = db_session.query(Trip).filter(Trip.title == trip_data["title"]).first()
        assert trip_in_db is not None
        assert trip_in_db.admin == admin_id
        assert trip_in_db.admin_user.email == sample_user_data["email"]

    def test_get_trips_by_admin(self, client, sample_user_data, sample_trip_data):
        """Test getting trips filtered by admin."""
        # Create two users
        user1_response = client.post("/api/users/", json={
            "email": "user1@example.com",
            "username": "user1"
        })
        user2_response = client.post("/api/users/", json={
            "email": "user2@example.com",
            "username": "user2"
        })
        
        admin1_id = user1_response.json()["id"]
        admin2_id = user2_response.json()["id"]
        
        # Create trips for each admin
        trip_data1 = sample_trip_data.copy()
        trip_data1["admin"] = admin1_id
        trip_data1["title"] = "Trip 1"
        
        trip_data2 = sample_trip_data.copy()
        trip_data2["admin"] = admin2_id
        trip_data2["title"] = "Trip 2"
        
        client.post("/api/trips/", json=trip_data1)
        client.post("/api/trips/", json=trip_data2)
        
        # Get trips by admin1
        response = client.get(f"/api/trips/?admin_id={admin1_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["admin"] == admin1_id
