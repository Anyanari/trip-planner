import pytest
from datetime import date, datetime
from app.models import User, Trip


class TestTrip:
    """Test cases for Trip model."""

    def test_trip_creation(self, db_session):
        """Test creating a trip with valid data."""
        # Create admin user first
        admin = User(email="admin@example.com", username="admin")
        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)

        trip = Trip(
            title="Test Trip",
            description="A test trip for testing",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=admin.id
        )
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(trip)

        assert trip.id is not None
        assert trip.title == "Test Trip"
        assert trip.description == "A test trip for testing"
        assert trip.start_date == date(2024, 6, 1)
        assert trip.end_date == date(2024, 6, 7)
        assert trip.admin == admin.id
        assert trip.created_time is not None
        assert isinstance(trip.created_time, datetime)
        assert trip.is_active is True

    def test_trip_title_required(self, db_session):
        """Test that title is required."""
        admin = User(email="admin@example.com", username="admin")
        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)

        trip = Trip(
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=admin.id
        )
        db_session.add(trip)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_trip_dates_required(self, db_session):
        """Test that start_date and end_date are required."""
        admin = User(email="admin@example.com", username="admin")
        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)

        # Test missing start_date
        trip1 = Trip(
            title="Test Trip",
            end_date=date(2024, 6, 7),
            admin=admin.id
        )
        db_session.add(trip1)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_trip_admin_required(self, db_session):
        """Test that admin is required."""
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7)
        )
        db_session.add(trip)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_trip_default_values(self, db_session):
        """Test default values for trip fields."""
        admin = User(email="admin@example.com", username="admin")
        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)

        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=admin.id
        )
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(trip)

        assert trip.is_active is True  # Default value
        assert trip.description is None  # Optional field

    def test_trip_relationships(self, db_session):
        """Test that trip relationships are properly set up."""
        admin = User(email="admin@example.com", username="admin")
        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)

        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=admin.id
        )
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(trip)

        # Test that relationship attributes exist
        assert hasattr(trip, 'admin_user')
        assert hasattr(trip, 'members')
        assert hasattr(trip, 'expenses')
        assert hasattr(trip, 'suggestions')
        assert hasattr(trip, 'routes')

    def test_trip_admin_user_relationship(self, db_session):
        """Test the relationship between trip and admin user."""
        admin = User(email="admin@example.com", username="admin")
        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)

        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=admin.id
        )
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(trip)

        # Test the relationship
        assert trip.admin_user.id == admin.id
        assert trip.admin_user.email == admin.email
        assert trip.admin_user.username == admin.username
