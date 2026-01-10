import pytest
from datetime import date, datetime
from app.models import User, Trip, TripMember


class TestTripMember:
    """Test cases for TripMember model."""

    def test_trip_member_creation(self, db_session):
        """Test creating a trip member with valid data."""
        admin = User(email="admin@example.com", username="admin")
        member = User(email="member@example.com", username="member")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=admin.id
        )
        db_session.add(admin)
        db_session.add(member)
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(admin)
        db_session.refresh(member)
        db_session.refresh(trip)

        trip_member = TripMember(
            trip_id=trip.id,
            user_id=member.id,
            role="member"
        )
        db_session.add(trip_member)
        db_session.commit()
        db_session.refresh(trip_member)

        assert trip_member.id is not None
        assert trip_member.trip_id == trip.id
        assert trip_member.user_id == member.id
        assert trip_member.role == "member"
        assert trip_member.joined_at is not None
        assert isinstance(trip_member.joined_at, datetime)

    def test_trip_member_default_role(self, db_session):
        """Test that role defaults to 'member'."""
        admin = User(email="admin@example.com", username="admin")
        member = User(email="member@example.com", username="member")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=admin.id
        )
        db_session.add(admin)
        db_session.add(member)
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(admin)
        db_session.refresh(member)
        db_session.refresh(trip)

        trip_member = TripMember(
            trip_id=trip.id,
            user_id=member.id
        )
        db_session.add(trip_member)
        db_session.commit()
        db_session.refresh(trip_member)

        assert trip_member.role == "member"

    def test_trip_member_required_fields(self, db_session):
        """Test that required fields are enforced."""
        admin = User(email="admin@example.com", username="admin")
        member = User(email="member@example.com", username="member")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=admin.id
        )
        db_session.add(admin)
        db_session.add(member)
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(admin)
        db_session.refresh(member)
        db_session.refresh(trip)

        # Test missing user_id
        trip_member1 = TripMember(
            trip_id=trip.id
        )
        db_session.add(trip_member1)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_trip_member_unique_constraint(self, db_session):
        """Test that a user can only be a member of a trip once."""
        admin = User(email="admin@example.com", username="admin")
        member = User(email="member@example.com", username="member")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=admin.id
        )
        db_session.add(admin)
        db_session.add(member)
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(admin)
        db_session.refresh(member)
        db_session.refresh(trip)

        # Add first membership
        trip_member1 = TripMember(
            trip_id=trip.id,
            user_id=member.id
        )
        db_session.add(trip_member1)
        db_session.commit()

        # Try to add duplicate membership
        trip_member2 = TripMember(
            trip_id=trip.id,
            user_id=member.id
        )
        db_session.add(trip_member2)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_trip_member_relationships(self, db_session):
        """Test that trip member relationships are properly set up."""
        admin = User(email="admin@example.com", username="admin")
        member = User(email="member@example.com", username="member")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=admin.id
        )
        db_session.add(admin)
        db_session.add(member)
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(admin)
        db_session.refresh(member)
        db_session.refresh(trip)

        trip_member = TripMember(
            trip_id=trip.id,
            user_id=member.id
        )
        db_session.add(trip_member)
        db_session.commit()
        db_session.refresh(trip_member)

        # Test that relationship attributes exist
        assert hasattr(trip_member, 'trip')
        assert hasattr(trip_member, 'user')

    def test_trip_member_trip_relationship(self, db_session):
        """Test the relationship between trip member and trip."""
        admin = User(email="admin@example.com", username="admin")
        member = User(email="member@example.com", username="member")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=admin.id
        )
        db_session.add(admin)
        db_session.add(member)
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(admin)
        db_session.refresh(member)
        db_session.refresh(trip)

        trip_member = TripMember(
            trip_id=trip.id,
            user_id=member.id
        )
        db_session.add(trip_member)
        db_session.commit()
        db_session.refresh(trip_member)

        # Test the relationship
        assert trip_member.trip.id == trip.id
        assert trip_member.trip.title == trip.title

    def test_trip_member_user_relationship(self, db_session):
        """Test the relationship between trip member and user."""
        admin = User(email="admin@example.com", username="admin")
        member = User(email="member@example.com", username="member")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=admin.id
        )
        db_session.add(admin)
        db_session.add(member)
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(admin)
        db_session.refresh(member)
        db_session.refresh(trip)

        trip_member = TripMember(
            trip_id=trip.id,
            user_id=member.id
        )
        db_session.add(trip_member)
        db_session.commit()
        db_session.refresh(trip_member)

        # Test the relationship
        assert trip_member.user.id == member.id
        assert trip_member.user.email == member.email
        assert trip_member.user.username == member.username

    def test_trip_member_different_roles(self, db_session):
        """Test different role values for trip members."""
        admin = User(email="admin@example.com", username="admin")
        member1 = User(email="member1@example.com", username="member1")
        member2 = User(email="member2@example.com", username="member2")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=admin.id
        )
        db_session.add(admin)
        db_session.add(member1)
        db_session.add(member2)
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(admin)
        db_session.refresh(member1)
        db_session.refresh(member2)
        db_session.refresh(trip)

        # Add member with default role
        trip_member1 = TripMember(
            trip_id=trip.id,
            user_id=member1.id
        )
        db_session.add(trip_member1)
        db_session.commit()
        db_session.refresh(trip_member1)

        # Add member with custom role
        trip_member2 = TripMember(
            trip_id=trip.id,
            user_id=member2.id,
            role="organizer"
        )
        db_session.add(trip_member2)
        db_session.commit()
        db_session.refresh(trip_member2)

        assert trip_member1.role == "member"
        assert trip_member2.role == "organizer"
