import pytest
from datetime import date, time
from decimal import Decimal
from fastapi.testclient import TestClient
from app.models import User, Trip, Place, Route


class TestRoutesRouter:
    """Test cases for routes router."""

    def test_create_route_success(self, client, sample_user_data, sample_trip_data):
        """Test successful route creation."""
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
        
        # Create route
        route_data = {
            "trip_id": trip_id,
            "place_id": place_id,
            "day_number": 1,
            "order_in_day": 1,
            "planned_time": "10:30:00",
            "estimated_cost": "150.50",
            "notes": "Visit this place in the morning",
            "added_by": user_id
        }
        
        response = client.post("/api/routes/", json=route_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["trip_id"] == route_data["trip_id"]
        assert data["place_id"] == route_data["place_id"]
        assert data["day_number"] == route_data["day_number"]
        assert data["order_in_day"] == route_data["order_in_day"]
        assert data["planned_time"] == route_data["planned_time"]
        assert data["estimated_cost"] == route_data["estimated_cost"]
        assert data["notes"] == route_data["notes"]
        assert data["added_by"] == route_data["added_by"]
        assert "id" in data
        assert "added_at" in data

    def test_create_route_minimal_data(self, client, sample_user_data, sample_trip_data):
        """Test route creation with minimal required data."""
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
        
        # Create route with minimal data
        route_data = {
            "trip_id": trip_id,
            "place_id": place_id,
            "day_number": 1,
            "order_in_day": 1
        }
        
        response = client.post("/api/routes/", json=route_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["trip_id"] == route_data["trip_id"]
        assert data["place_id"] == route_data["place_id"]
        assert data["day_number"] == route_data["day_number"]
        assert data["order_in_day"] == route_data["order_in_day"]
        assert data["planned_time"] is None  # Optional field
        assert data["estimated_cost"] is None  # Optional field
        assert data["notes"] is None  # Optional field
        assert data["added_by"] is None  # Optional field

    def test_create_route_missing_fields(self, client, sample_user_data, sample_trip_data):
        """Test route creation with missing required fields."""
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
        
        # Missing day_number
        route_data = {
            "trip_id": trip_id,
            "place_id": place_id,
            "order_in_day": 1
        }
        response = client.post("/api/routes/", json=route_data)
        assert response.status_code == 422

    def test_create_route_nonexistent_trip(self, client, sample_user_data):
        """Test route creation with non-existent trip."""
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
        
        route_data = {
            "trip_id": 99999,
            "place_id": place_id,
            "day_number": 1,
            "order_in_day": 1
        }
        
        response = client.post("/api/routes/", json=route_data)
        assert response.status_code in [400, 422]

    def test_get_routes_empty(self, client):
        """Test getting routes when database is empty."""
        response = client.get("/api/routes/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_routes_with_data(self, client, sample_user_data, sample_trip_data):
        """Test getting routes when database has data."""
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
        
        # Create some routes
        routes_data = [
            {
                "trip_id": trip_id,
                "place_id": place_id,
                "day_number": i + 1,
                "order_in_day": 1
            }
            for i in range(3)
        ]
        
        for route_data in routes_data:
            client.post("/api/routes/", json=route_data)
        
        response = client.get("/api/routes/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

    def test_get_routes_by_trip(self, client, sample_user_data, sample_trip_data):
        """Test getting routes filtered by trip."""
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
        
        # Create routes for each trip
        route_data1 = {
            "trip_id": trip_id1,
            "place_id": place_id,
            "day_number": 1,
            "order_in_day": 1
        }
        
        route_data2 = {
            "trip_id": trip_id2,
            "place_id": place_id,
            "day_number": 1,
            "order_in_day": 1
        }
        
        client.post("/api/routes/", json=route_data1)
        client.post("/api/routes/", json=route_data2)
        
        # Get routes for trip 1
        response = client.get(f"/api/routes/?trip_id={trip_id1}")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["trip_id"] == trip_id1

    def test_get_routes_by_day(self, client, sample_user_data, sample_trip_data):
        """Test getting routes filtered by day number."""
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
        
        # Create routes for different days
        routes_data = [
            {
                "trip_id": trip_id,
                "place_id": place_id,
                "day_number": 1,
                "order_in_day": 1
            },
            {
                "trip_id": trip_id,
                "place_id": place_id,
                "day_number": 2,
                "order_in_day": 1
            },
            {
                "trip_id": trip_id,
                "place_id": place_id,
                "day_number": 1,
                "order_in_day": 2
            }
        ]
        
        for route_data in routes_data:
            client.post("/api/routes/", json=route_data)
        
        # Get routes for day 1
        response = client.get(f"/api/routes/?trip_id={trip_id}&day_number=1")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert all(route["day_number"] == 1 for route in data)

    def test_get_route_by_id_success(self, client, sample_user_data, sample_trip_data):
        """Test getting a route by ID."""
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
        
        # Create route
        route_data = {
            "trip_id": trip_id,
            "place_id": place_id,
            "day_number": 1,
            "order_in_day": 1
        }
        create_response = client.post("/api/routes/", json=route_data)
        route_id = create_response.json()["id"]
        
        # Get route
        response = client.get(f"/api/routes/{route_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == route_id
        assert data["trip_id"] == trip_id

    def test_get_route_by_id_not_found(self, client):
        """Test getting a non-existent route by ID."""
        response = client.get("/api/routes/99999")
        
        assert response.status_code == 404
        assert "Route not found" in response.json()["detail"]

    def test_update_route_success(self, client, sample_user_data, sample_trip_data):
        """Test updating a route."""
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
        
        # Create route
        route_data = {
            "trip_id": trip_id,
            "place_id": place_id,
            "day_number": 1,
            "order_in_day": 1
        }
        create_response = client.post("/api/routes/", json=route_data)
        route_id = create_response.json()["id"]
        
        # Update route
        update_data = {
            "planned_time": "14:30:00",
            "estimated_cost": "200.00",
            "notes": "Updated notes"
        }
        response = client.put(f"/api/routes/{route_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["planned_time"] == update_data["planned_time"]
        assert data["estimated_cost"] == update_data["estimated_cost"]
        assert data["notes"] == update_data["notes"]

    def test_update_route_not_found(self, client):
        """Test updating a non-existent route."""
        update_data = {
            "planned_time": "14:30:00"
        }
        response = client.put("/api/routes/99999", json=update_data)
        
        assert response.status_code == 404

    def test_delete_route_success(self, client, sample_user_data, sample_trip_data):
        """Test deleting a route."""
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
        
        # Create route
        route_data = {
            "trip_id": trip_id,
            "place_id": place_id,
            "day_number": 1,
            "order_in_day": 1
        }
        create_response = client.post("/api/routes/", json=route_data)
        route_id = create_response.json()["id"]
        
        # Delete route
        response = client.delete(f"/api/routes/{route_id}")
        
        assert response.status_code == 200
        
        # Verify route is deleted
        get_response = client.get(f"/api/routes/{route_id}")
        assert get_response.status_code == 404

    def test_delete_route_not_found(self, client):
        """Test deleting a non-existent route."""
        response = client.delete("/api/routes/99999")
        
        assert response.status_code == 404

    def test_route_data_persistence(self, client, sample_user_data, sample_trip_data, db_session):
        """Test that route data is properly persisted in database."""
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
        
        # Create route via API
        route_data = {
            "trip_id": trip_id,
            "place_id": place_id,
            "day_number": 1,
            "order_in_day": 1,
            "planned_time": "10:30:00",
            "estimated_cost": "150.50",
            "notes": "Test notes",
            "added_by": user_id
        }
        
        response = client.post("/api/routes/", json=route_data)
        assert response.status_code == 200
        
        # Check that route exists in database
        route_in_db = db_session.query(Route).filter(
            Route.trip_id == trip_id
        ).first()
        
        assert route_in_db is not None
        assert route_in_db.trip_id == trip_id
        assert route_in_db.place_id == place_id
        assert route_in_db.day_number == 1
        assert route_in_db.order_in_day == 1
        assert route_in_db.planned_time == time(10, 30)
        assert route_in_db.estimated_cost == Decimal("150.50")
        assert route_in_db.notes == "Test notes"
        assert route_in_db.added_by == user_id
