import pytest
from datetime import date, datetime, time
from decimal import Decimal
from app.models import User, Trip, Place, Route


class TestRoute:
    """Test cases for Route model."""

    def test_route_creation(self, db_session):
        """Test creating a route with valid data."""
        user = User(email="test@example.com", username="testuser")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=user.id
        )
        place = Place(
            name="Test Place",
            lat="55.7558",
            lng="37.6173"
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.add(place)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)
        db_session.refresh(place)

        route = Route(
            trip_id=trip.id,
            place_id=place.id,
            day_number=1,
            order_in_day=1,
            planned_time=time(10, 30),
            estimated_cost=Decimal('150.50'),
            notes="Visit this place in the morning",
            added_by=user.id
        )
        db_session.add(route)
        db_session.commit()
        db_session.refresh(route)

        assert route.id is not None
        assert route.trip_id == trip.id
        assert route.place_id == place.id
        assert route.day_number == 1
        assert route.order_in_day == 1
        assert route.planned_time == time(10, 30)
        assert route.estimated_cost == Decimal('150.50')
        assert route.notes == "Visit this place in the morning"
        assert route.added_by == user.id
        assert route.added_at is not None
        assert isinstance(route.added_at, datetime)

    def test_route_required_fields(self, db_session):
        """Test that required fields are enforced."""
        user = User(email="test@example.com", username="testuser")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=user.id
        )
        place = Place(
            name="Test Place",
            lat="55.7558",
            lng="37.6173"
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.add(place)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)
        db_session.refresh(place)

        # Test missing day_number
        route1 = Route(
            trip_id=trip.id,
            place_id=place.id,
            order_in_day=1
        )
        db_session.add(route1)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_route_optional_fields(self, db_session):
        """Test optional fields for route."""
        user = User(email="test@example.com", username="testuser")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=user.id
        )
        place = Place(
            name="Test Place",
            lat="55.7558",
            lng="37.6173"
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.add(place)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)
        db_session.refresh(place)

        route = Route(
            trip_id=trip.id,
            place_id=place.id,
            day_number=1,
            order_in_day=1
        )
        db_session.add(route)
        db_session.commit()
        db_session.refresh(route)

        assert route.planned_time is None  # Optional field
        assert route.estimated_cost is None  # Optional field
        assert route.notes is None  # Optional field
        assert route.added_by is None  # Optional field

    def test_route_relationships(self, db_session):
        """Test that route relationships are properly set up."""
        user = User(email="test@example.com", username="testuser")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=user.id
        )
        place = Place(
            name="Test Place",
            lat="55.7558",
            lng="37.6173"
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.add(place)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)
        db_session.refresh(place)

        route = Route(
            trip_id=trip.id,
            place_id=place.id,
            day_number=1,
            order_in_day=1
        )
        db_session.add(route)
        db_session.commit()
        db_session.refresh(route)

        # Test that relationship attributes exist
        assert hasattr(route, 'trip')
        assert hasattr(route, 'place')
        assert hasattr(route, 'added_by_user')

    def test_route_trip_relationship(self, db_session):
        """Test the relationship between route and trip."""
        user = User(email="test@example.com", username="testuser")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=user.id
        )
        place = Place(
            name="Test Place",
            lat="55.7558",
            lng="37.6173"
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.add(place)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)
        db_session.refresh(place)

        route = Route(
            trip_id=trip.id,
            place_id=place.id,
            day_number=1,
            order_in_day=1
        )
        db_session.add(route)
        db_session.commit()
        db_session.refresh(route)

        # Test the relationship
        assert route.trip.id == trip.id
        assert route.trip.title == trip.title

    def test_route_place_relationship(self, db_session):
        """Test the relationship between route and place."""
        user = User(email="test@example.com", username="testuser")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=user.id
        )
        place = Place(
            name="Test Place",
            lat="55.7558",
            lng="37.6173"
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.add(place)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)
        db_session.refresh(place)

        route = Route(
            trip_id=trip.id,
            place_id=place.id,
            day_number=1,
            order_in_day=1
        )
        db_session.add(route)
        db_session.commit()
        db_session.refresh(route)

        # Test the relationship
        assert route.place.id == place.id
        assert route.place.name == place.name

    def test_route_added_by_user_relationship(self, db_session):
        """Test the relationship between route and added_by user."""
        user = User(email="test@example.com", username="testuser")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=user.id
        )
        place = Place(
            name="Test Place",
            lat="55.7558",
            lng="37.6173"
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.add(place)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)
        db_session.refresh(place)

        route = Route(
            trip_id=trip.id,
            place_id=place.id,
            day_number=1,
            order_in_day=1,
            added_by=user.id
        )
        db_session.add(route)
        db_session.commit()
        db_session.refresh(route)

        # Test the relationship
        assert route.added_by_user.id == user.id
        assert route.added_by_user.email == user.email

    def test_route_time_handling(self, db_session):
        """Test time field handling."""
        user = User(email="test@example.com", username="testuser")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=user.id
        )
        place = Place(
            name="Test Place",
            lat="55.7558",
            lng="37.6173"
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.add(place)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)
        db_session.refresh(place)

        route = Route(
            trip_id=trip.id,
            place_id=place.id,
            day_number=1,
            order_in_day=1,
            planned_time=time(14, 45, 30)
        )
        db_session.add(route)
        db_session.commit()
        db_session.refresh(route)

        assert route.planned_time == time(14, 45, 30)
