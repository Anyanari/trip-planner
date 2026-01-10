import pytest
from decimal import Decimal
from datetime import date
from fastapi.testclient import TestClient
from app.models import User, Trip, Expense


class TestExpensesRouter:
    """Test cases for expenses router."""

    def test_create_expense_success(self, client, sample_user_data, sample_trip_data):
        """Test successful expense creation."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Create expense
        expense_data = {
            "trip_id": trip_id,
            "title": "Dinner at Restaurant",
            "amount": "150.50",
            "currency": "RUB",
            "paid_by": user_id,
            "date": "2026-01-09",
            "shares": [
                {"user_id": user_id, "share": 1.0}
            ]
        }
        
        response = client.post("/api/expenses/", json=expense_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["trip_id"] == expense_data["trip_id"]
        assert data["title"] == expense_data["title"]
        assert data["amount"] == expense_data["amount"]
        assert data["currency"] == expense_data["currency"]
        assert data["paid_by"] == expense_data["paid_by"]
        assert "id" in data
        assert "created_at" in data

    def test_create_expense_default_currency(self, client, sample_user_data, sample_trip_data):
        """Test expense creation with default currency."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Create expense without currency
        expense_data = {
            "trip_id": trip_id,
            "title": "Test Expense",
            "amount": "100.00",
            "paid_by": user_id
        }
        
        response = client.post("/api/expenses/", json=expense_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["currency"] == "RUB"  # Default currency

    def test_create_expense_missing_fields(self, client, sample_user_data, sample_trip_data):
        """Test expense creation with missing required fields."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Missing title
        expense_data = {
            "trip_id": trip_id,
            "amount": "100.00",
            "paid_by": user_id
        }
        response = client.post("/api/expenses/", json=expense_data)
        assert response.status_code == 422

    def test_create_expense_nonexistent_trip(self, client, sample_user_data):
        """Test expense creation with non-existent trip."""
        # Create user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        expense_data = {
            "trip_id": 99999,
            "title": "Test Expense",
            "amount": "100.00",
            "paid_by": user_id
        }
        
        response = client.post("/api/expenses/", json=expense_data)
        assert response.status_code in [400, 422]

    def test_create_expense_nonexistent_user(self, client, sample_user_data, sample_trip_data):
        """Test expense creation with non-existent user."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        expense_data = {
            "trip_id": trip_id,
            "title": "Test Expense",
            "amount": "100.00",
            "paid_by": 99999
        }
        
        response = client.post("/api/expenses/", json=expense_data)
        assert response.status_code in [400, 422]

    def test_get_expenses_empty(self, client):
        """Test getting expenses when database is empty."""
        response = client.get("/api/expenses/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_expenses_with_data(self, client, sample_user_data, sample_trip_data):
        """Test getting expenses when database has data."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Create some expenses
        expenses_data = [
            {
                "trip_id": trip_id,
                "title": f"Expense {i}",
                "amount": f"{100 + i}.00",
                "paid_by": user_id
            }
            for i in range(3)
        ]
        
        for expense_data in expenses_data:
            client.post("/api/expenses/", json=expense_data)
        
        response = client.get("/api/expenses/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

    def test_get_expenses_by_trip(self, client, sample_user_data, sample_trip_data):
        """Test getting expenses filtered by trip."""
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
        
        # Create expenses for each trip
        expense_data1 = {
            "trip_id": trip_id1,
            "title": "Expense 1",
            "amount": "100.00",
            "paid_by": user_id
        }
        
        expense_data2 = {
            "trip_id": trip_id2,
            "title": "Expense 2",
            "amount": "200.00",
            "paid_by": user_id
        }
        
        client.post("/api/expenses/", json=expense_data1)
        client.post("/api/expenses/", json=expense_data2)
        
        # Get expenses for trip 1
        response = client.get(f"/api/expenses/?trip_id={trip_id1}")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["trip_id"] == trip_id1

    def test_get_expense_by_id_success(self, client, sample_user_data, sample_trip_data):
        """Test getting an expense by ID."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Create expense
        expense_data = {
            "trip_id": trip_id,
            "title": "Test Expense",
            "amount": "100.00",
            "paid_by": user_id
        }
        create_response = client.post("/api/expenses/", json=expense_data)
        expense_id = create_response.json()["id"]
        
        # Get expense
        response = client.get(f"/api/expenses/{expense_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == expense_id
        assert data["title"] == expense_data["title"]

    def test_get_expense_by_id_not_found(self, client):
        """Test getting a non-existent expense by ID."""
        response = client.get("/api/expenses/99999")
        
        assert response.status_code == 404
        assert "Expense not found" in response.json()["detail"]

    def test_update_expense_success(self, client, sample_user_data, sample_trip_data):
        """Test updating an expense."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Create expense
        expense_data = {
            "trip_id": trip_id,
            "title": "Original Expense",
            "amount": "100.00",
            "paid_by": user_id
        }
        create_response = client.post("/api/expenses/", json=expense_data)
        expense_id = create_response.json()["id"]
        
        # Update expense
        update_data = {
            "title": "Updated Expense",
            "amount": "150.00"
        }
        response = client.put(f"/api/expenses/{expense_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["amount"] == update_data["amount"]

    def test_update_expense_not_found(self, client):
        """Test updating a non-existent expense."""
        update_data = {
            "title": "Updated Title"
        }
        response = client.put("/api/expenses/99999", json=update_data)
        
        assert response.status_code == 404

    def test_delete_expense_success(self, client, sample_user_data, sample_trip_data):
        """Test deleting an expense."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Create expense
        expense_data = {
            "trip_id": trip_id,
            "title": "Test Expense",
            "amount": "100.00",
            "paid_by": user_id
        }
        create_response = client.post("/api/expenses/", json=expense_data)
        expense_id = create_response.json()["id"]
        
        # Delete expense
        response = client.delete(f"/api/expenses/{expense_id}")
        
        assert response.status_code == 200
        
        # Verify expense is deleted
        get_response = client.get(f"/api/expenses/{expense_id}")
        assert get_response.status_code == 404

    def test_delete_expense_not_found(self, client):
        """Test deleting a non-existent expense."""
        response = client.delete("/api/expenses/99999")
        
        assert response.status_code == 404

    def test_expense_data_persistence(self, client, sample_user_data, sample_trip_data, db_session):
        """Test that expense data is properly persisted in database."""
        # Create admin user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create trip
        trip_data = sample_trip_data.copy()
        trip_data["admin"] = user_id
        trip_response = client.post("/api/trips/", json=trip_data)
        trip_id = trip_response.json()["id"]
        
        # Create expense via API
        expense_data = {
            "trip_id": trip_id,
            "title": "Test Expense",
            "amount": "150.50",
            "currency": "USD",
            "paid_by": user_id
        }
        
        response = client.post("/api/expenses/", json=expense_data)
        assert response.status_code == 200
        
        # Check that expense exists in database
        expense_in_db = db_session.query(Expense).filter(
            Expense.title == expense_data["title"]
        ).first()
        
        assert expense_in_db is not None
        assert expense_in_db.trip_id == trip_id
        assert expense_in_db.title == expense_data["title"]
        assert expense_in_db.amount == Decimal(expense_data["amount"])
        assert expense_in_db.currency == expense_data["currency"]
        assert expense_in_db.paid_by == user_id
