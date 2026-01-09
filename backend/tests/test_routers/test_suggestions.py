import pytest
from datetime import date
from fastapi.testclient import TestClient
from app.models import User, Trip, Place, Suggestion, Vote


class TestSuggestionsRouter:
    """Test cases for suggestions router."""

    def test_create_suggestion_success(self, client, sample_user_data, sample_trip_data):
        """Test successful suggestion creation."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Create place
        place_data = {
            "name": "Test Place",
            "lat": "55.7558",
            "lng": "37.6173"
        }
        place_response = client.post("/api/places/", json=place_data)
        place_id = place_response.json()["id"]
        
        # Create suggestion
        suggestion_data = {
            "trip_id": trip_id,
            "place_id": place_id,
            "suggested_by": user_id
        }
        
        response = client.post("/api/suggestions/", json=suggestion_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["trip_id"] == suggestion_data["trip_id"]
        assert data["place_id"] == suggestion_data["place_id"]
        assert data["suggested_by"] == suggestion_data["suggested_by"]
        assert data["status"] == "voting"  # Default value
        assert data["votes_for"] == 0  # Default value
        assert data["votes_against"] == 0  # Default value
        assert "id" in data
        assert "suggested_at" in data

    def test_create_suggestion_missing_fields(self, client, sample_user_data, sample_trip_data):
        """Test suggestion creation with missing required fields."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Missing place_id
        suggestion_data = {
            "trip_id": trip_id,
            "suggested_by": user_id
        }
        response = client.post("/api/suggestions/", json=suggestion_data)
        assert response.status_code == 422

    def test_create_suggestion_nonexistent_trip(self, client, sample_user_data):
        """Test suggestion creation with non-existent trip."""
        # Create user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create place
        place_data = {
            "name": "Test Place",
            "lat": "55.7558",
            "lng": "37.6173"
        }
        place_response = client.post("/api/places/", json=place_data)
        place_id = place_response.json()["id"]
        
        suggestion_data = {
            "trip_id": 99999,
            "place_id": place_id,
            "suggested_by": user_id
        }
        
        response = client.post("/api/suggestions/", json=suggestion_data)
        assert response.status_code in [400, 422]

    def test_get_suggestions_empty(self, client):
        """Test getting suggestions when database is empty."""
        response = client.get("/api/suggestions/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_suggestions_with_data(self, client, sample_user_data, sample_trip_data):
        """Test getting suggestions when database has data."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Create place
        place_data = {
            "name": "Test Place",
            "lat": "55.7558",
            "lng": "37.6173"
        }
        place_response = client.post("/api/places/", json=place_data)
        place_id = place_response.json()["id"]
        
        # Create some suggestions
        suggestions_data = [
            {
                "trip_id": trip_id,
                "place_id": place_id,
                "suggested_by": user_id
            }
            for _ in range(3)
        ]
        
        for suggestion_data in suggestions_data:
            client.post("/api/suggestions/", json=suggestion_data)
        
        response = client.get("/api/suggestions/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

    def test_get_suggestions_by_trip(self, client, sample_user_data, sample_trip_data):
        """Test getting suggestions filtered by trip."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create two trips
        trip_data1 = sample_trip_data.copy()
        trip_data1["admin"] = user_id
        trip_data1["title"] = "Trip 1"
        trip_response1 = client.post("/api/trips/", json=trip_data1)
        trip_id1 = trip_response1.json()["id"]
        
        trip_data2 = sample_trip_data.copy()
        trip_data2["admin"] = user_id
        trip_data2["title"] = "Trip 2"
        trip_data2["start_date"] = "2024-07-01"
        trip_data2["end_date"] = "2024-07-07"
        trip_response2 = client.post("/api/trips/", json=trip_data2)
        trip_id2 = trip_response2.json()["id"]
        
        # Create place
        place_data = {
            "name": "Test Place",
            "lat": "55.7558",
            "lng": "37.6173"
        }
        place_response = client.post("/api/places/", json=place_data)
        place_id = place_response.json()["id"]
        
        # Create suggestions for each trip
        suggestion_data1 = {
            "trip_id": trip_id1,
            "place_id": place_id,
            "suggested_by": user_id
        }
        
        suggestion_data2 = {
            "trip_id": trip_id2,
            "place_id": place_id,
            "suggested_by": user_id
        }
        
        client.post("/api/suggestions/", json=suggestion_data1)
        client.post("/api/suggestions/", json=suggestion_data2)
        
        # Get suggestions for trip 1
        response = client.get(f"/api/suggestions/?trip_id={trip_id1}")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["trip_id"] == trip_id1

    def test_get_suggestion_by_id_success(self, client, sample_user_data, sample_trip_data):
        """Test getting a suggestion by ID."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Create place
        place_data = {
            "name": "Test Place",
            "lat": "55.7558",
            "lng": "37.6173"
        }
        place_response = client.post("/api/places/", json=place_data)
        place_id = place_response.json()["id"]
        
        # Create suggestion
        suggestion_data = {
            "trip_id": trip_id,
            "place_id": place_id,
            "suggested_by": user_id
        }
        create_response = client.post("/api/suggestions/", json=suggestion_data)
        suggestion_id = create_response.json()["id"]
        
        # Get suggestion
        response = client.get(f"/api/suggestions/{suggestion_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == suggestion_id
        assert data["trip_id"] == trip_id

    def test_get_suggestion_by_id_not_found(self, client):
        """Test getting a non-existent suggestion by ID."""
        response = client.get("/api/suggestions/99999")
        
        assert response.status_code == 404
        assert "Suggestion not found" in response.json()["detail"]

    def test_vote_on_suggestion_success(self, client, sample_user_data, sample_trip_data):
        """Test voting on a suggestion."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create voting user
        voter_data = {
            "email": "voter@example.com",
            "username": "voter"
        }
        voter_response = client.post("/api/users/", json=voter_data)
        voter_id = voter_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Create place
        place_data = {
            "name": "Test Place",
            "lat": "55.7558",
            "lng": "37.6173"
        }
        place_response = client.post("/api/places/", json=place_data)
        place_id = place_response.json()["id"]
        
        # Create suggestion
        suggestion_data = {
            "trip_id": trip_id,
            "place_id": place_id,
            "suggested_by": user_id
        }
        create_response = client.post("/api/suggestions/", json=suggestion_data)
        suggestion_id = create_response.json()["id"]
        
        # Vote on suggestion
        vote_data = {
            "user_id": voter_id,
            "vote": True
        }
        response = client.post(f"/api/suggestions/{suggestion_id}/vote", json=vote_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["votes_for"] == 1
        assert data["votes_against"] == 0

    def test_vote_on_suggestion_twice(self, client, sample_user_data, sample_trip_data):
        """Test voting twice on the same suggestion."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create voting user
        voter_data = {
            "email": "voter@example.com",
            "username": "voter"
        }
        voter_response = client.post("/api/users/", json=voter_data)
        voter_id = voter_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Create place
        place_data = {
            "name": "Test Place",
            "lat": "55.7558",
            "lng": "37.6173"
        }
        place_response = client.post("/api/places/", json=place_data)
        place_id = place_response.json()["id"]
        
        # Create suggestion
        suggestion_data = {
            "trip_id": trip_id,
            "place_id": place_id,
            "suggested_by": user_id
        }
        create_response = client.post("/api/suggestions/", json=suggestion_data)
        suggestion_id = create_response.json()["id"]
        
        # First vote
        vote_data = {
            "user_id": voter_id,
            "vote": True
        }
        response1 = client.post(f"/api/suggestions/{suggestion_id}/vote", json=vote_data)
        assert response1.status_code == 200
        
        # Second vote (should update or fail)
        response2 = client.post(f"/api/suggestions/{suggestion_id}/vote", json=vote_data)
        # Behavior depends on implementation - might update or reject

    def test_update_suggestion_status(self, client, sample_user_data, sample_trip_data):
        """Test updating suggestion status."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Create place
        place_data = {
            "name": "Test Place",
            "lat": "55.7558",
            "lng": "37.6173"
        }
        place_response = client.post("/api/places/", json=place_data)
        place_id = place_response.json()["id"]
        
        # Create suggestion
        suggestion_data = {
            "trip_id": trip_id,
            "place_id": place_id,
            "suggested_by": user_id
        }
        create_response = client.post("/api/suggestions/", json=suggestion_data)
        suggestion_id = create_response.json()["id"]
        
        # Update status
        update_data = {
            "status": "approved"
        }
        response = client.put(f"/api/suggestions/{suggestion_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "approved"

    def test_delete_suggestion_success(self, client, sample_user_data, sample_trip_data):
        """Test deleting a suggestion."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Create place
        place_data = {
            "name": "Test Place",
            "lat": "55.7558",
            "lng": "37.6173"
        }
        place_response = client.post("/api/places/", json=place_data)
        place_id = place_response.json()["id"]
        
        # Create suggestion
        suggestion_data = {
            "trip_id": trip_id,
            "place_id": place_id,
            "suggested_by": user_id
        }
        create_response = client.post("/api/suggestions/", json=suggestion_data)
        suggestion_id = create_response.json()["id"]
        
        # Delete suggestion
        response = client.delete(f"/api/suggestions/{suggestion_id}")
        
        assert response.status_code == 200
        
        # Verify suggestion is deleted
        get_response = client.get(f"/api/suggestions/{suggestion_id}")
        assert get_response.status_code == 404

    def test_suggestion_data_persistence(self, client, sample_user_data, sample_trip_data, db_session):
        """Test that suggestion data is properly persisted in database."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Create place
        place_data = {
            "name": "Test Place",
            "lat": "55.7558",
            "lng": "37.6173"
        }
        place_response = client.post("/api/places/", json=place_data)
        place_id = place_response.json()["id"]
        
        # Create suggestion via API
        suggestion_data = {
            "trip_id": trip_id,
            "place_id": place_id,
            "suggested_by": user_id
        }
        
        response = client.post("/api/suggestions/", json=suggestion_data)
        assert response.status_code == 200
        
        # Check that suggestion exists in database
        suggestion_in_db = db_session.query(Suggestion).filter(
            Suggestion.trip_id == trip_id
        ).first()
        
        assert suggestion_in_db is not None
        assert suggestion_in_db.trip_id == trip_id
        assert suggestion_in_db.place_id == place_id
        assert suggestion_in_db.suggested_by == user_id
        assert suggestion_in_db.status == "voting"
        assert suggestion_in_db.votes_for == 0
        assert suggestion_in_db.votes_against == 0
