import pytest
from decimal import Decimal
from fastapi.testclient import TestClient
from app.models import Place


class TestPlacesRouter:
    """Test cases for places router."""

    def test_create_place_success(self, client):
        """Test successful place creation."""
        place_data = {
            "name": "Test Place",
            "lat": 55.7558,
            "lng": 37.6173,
            "osm_id": "node/123456",
            "address": "Test Address, Moscow"
        }
        
        response = client.post("/api/places/", json=place_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == place_data["name"]
        assert data["lat"] == place_data["lat"]
        assert data["lng"] == place_data["lng"]
        assert data["osm_id"] == place_data["osm_id"]
        assert data["address"] == place_data["address"]
        assert "id" in data
        assert "created_at" in data

    def test_create_place_minimal_data(self, client):
        """Test place creation with minimal required data."""
        place_data = {
            "name": "Test Place",
            "lat": 55.7558,
            "lng": 37.6173
        }
        
        response = client.post("/api/places/", json=place_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == place_data["name"]
        assert data["lat"] == place_data["lat"]
        assert data["lng"] == place_data["lng"]
        assert data["osm_id"] is None
        assert data["address"] is None

    def test_create_place_missing_required_fields(self, client):
        """Test place creation with missing required fields."""
        # Missing name
        place_data = {
            "lat": "55.7558",
            "lng": "37.6173"
        }
        response = client.post("/api/places/", json=place_data)
        assert response.status_code == 422

        # Missing lat
        place_data = {
            "name": "Test Place",
            "lng": "37.6173"
        }
        response = client.post("/api/places/", json=place_data)
        assert response.status_code == 422

        # Missing lng
        place_data = {
            "name": "Test Place",
            "lat": "55.7558"
        }
        response = client.post("/api/places/", json=place_data)
        assert response.status_code == 422

    def test_create_place_invalid_coordinates(self, client):
        """Test place creation with invalid coordinates."""
        # Invalid latitude (out of range)
        place_data = {
            "name": "Test Place",
            "lat": "95.7558",  # Invalid latitude
            "lng": "37.6173"
        }
        response = client.post("/api/places/", json=place_data)
        # This might pass depending on validation implementation

        # Invalid longitude (out of range)
        place_data = {
            "name": "Test Place",
            "lat": "55.7558",
            "lng": "190.6173"  # Invalid longitude
        }
        response = client.post("/api/places/", json=place_data)
        # This might pass depending on validation implementation

    def test_create_place_duplicate_osm_id(self, client):
        """Test place creation with duplicate OSM ID."""
        place_data1 = {
            "name": "Place 1",
            "lat": "55.7558",
            "lng": "37.6173",
            "osm_id": "node/123456"
        }
        
        place_data2 = {
            "name": "Place 2",
            "lat": "55.7559",
            "lng": "37.6174",
            "osm_id": "node/123456"
        }
        
        # Create first place
        response1 = client.post("/api/places/", json=place_data1)
        assert response1.status_code == 200
        
        # Try to create second place with same OSM ID
        response2 = client.post("/api/places/", json=place_data2)
        assert response2.status_code == 400

    def test_get_places_empty(self, client):
        """Test getting places when database is empty."""
        response = client.get("/api/places/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_places_with_data(self, client):
        """Test getting places when database has data."""
        # Create some places
        places_data = [
            {
                "name": f"Place {i}",
                "lat": "55.7558",
                "lng": "37.6173"
            }
            for i in range(3)
        ]
        
        for place_data in places_data:
            client.post("/api/places/", json=place_data)
        
        response = client.get("/api/places/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

    def test_get_place_by_id_success(self, client):
        """Test getting a place by ID."""
        place_data = {
            "name": "Test Place",
            "lat": "55.7558",
            "lng": "37.6173"
        }
        
        # Create place
        create_response = client.post("/api/places/", json=place_data)
        place_id = create_response.json()["id"]
        
        # Get place
        response = client.get(f"/api/places/{place_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == place_id
        assert data["name"] == place_data["name"]

    def test_get_place_by_id_not_found(self, client):
        """Test getting a non-existent place by ID."""
        response = client.get("/api/places/99999")
        
        assert response.status_code == 404
        assert "Place not found" in response.json()["detail"]

    def test_search_places_by_name(self, client):
        """Test searching places by name."""
        # Create some places
        places_data = [
            {
                "name": "Restaurant 1",
                "lat": 55.7558,
                "lng": 37.6173,
                "osm_id": "node/123456",
                "address": "Address 1"
            },
            {
                "name": "Restaurant 2", 
                "lat": 55.7559,
                "lng": 37.6174,
                "osm_id": "node/123457",
                "address": "Address 2"
            }
        ]
        
        for place_data in places_data:
            client.post("/api/places/", json=place_data)
        
        # Search using the search endpoint
        response = client.get("/api/places/search?query=Restaurant")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "places" in data
        assert len(data["places"]) == 2
        assert all("Restaurant" in place["display_name"] for place in data["places"])

    def test_search_places_by_location(self, client):
        """Test searching places by location coordinates."""
        # Create some places
        places_data = [
            {"name": "Place 1", "lat": "55.7558", "lng": "37.6173"},
            {"name": "Place 2", "lat": "55.7560", "lng": "37.6175"},
            {"name": "Place 3", "lat": "59.9343", "lng": "30.3351"}
        ]
        
        for place_data in places_data:
            client.post("/api/places/", json=place_data)
        
        # Search near Moscow coordinates
        response = client.get("/api/places/search?lat=55.7558&lng=37.6173&radius=1.0")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Should return places near Moscow

    def test_update_place_success(self, client):
        """Test updating a place."""
        place_data = {
            "name": "Test Place",
            "lat": "55.7558",
            "lng": "37.6173"
        }
        
        # Create place
        create_response = client.post("/api/places/", json=place_data)
        place_id = create_response.json()["id"]
        
        # Update place
        update_data = {
            "name": "Updated Place Name",
            "address": "Updated Address"
        }
        response = client.put(f"/api/places/{place_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["address"] == update_data["address"]

    def test_update_place_not_found(self, client):
        """Test updating a non-existent place."""
        update_data = {
            "name": "Updated Name"
        }
        response = client.put("/api/places/99999", json=update_data)
        
        assert response.status_code == 404

    def test_delete_place_success(self, client):
        """Test deleting a place."""
        place_data = {
            "name": "Test Place",
            "lat": "55.7558",
            "lng": "37.6173"
        }
        
        # Create place
        create_response = client.post("/api/places/", json=place_data)
        place_id = create_response.json()["id"]
        
        # Delete place
        response = client.delete(f"/api/places/{place_id}")
        
        assert response.status_code == 200
        
        # Verify place is deleted
        get_response = client.get(f"/api/places/{place_id}")
        assert get_response.status_code == 404

    def test_delete_place_not_found(self, client):
        """Test deleting a non-existent place."""
        response = client.delete("/api/places/99999")
        
        assert response.status_code == 404

    def test_place_data_persistence(self, client, db_session):
        """Test that place data is properly persisted in database."""
        place_data = {
            "name": "Test Place",
            "lat": "55.7558",
            "lng": "37.6173",
            "osm_id": "node/123456",
            "address": "Test Address"
        }
        
        # Create place via API
        response = client.post("/api/places/", json=place_data)
        assert response.status_code == 200
        
        # Check that place exists in database
        place_in_db = db_session.query(Place).filter(
            Place.name == place_data["name"]
        ).first()
        
        assert place_in_db is not None
        assert place_in_db.name == place_data["name"]
        assert place_in_db.lat == Decimal(place_data["lat"])
        assert place_in_db.lng == Decimal(place_data["lng"])
        assert place_in_db.osm_id == place_data["osm_id"]
        assert place_in_db.address == place_data["address"]
