import pytest
from datetime import date, datetime
from app.models import User, Trip, Place, Suggestion, Vote


class TestSuggestion:
    """Test cases for Suggestion model."""

    def test_suggestion_creation(self, db_session):
        """Test creating a suggestion with valid data."""
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

        suggestion = Suggestion(
            trip_id=trip.id,
            place_id=place.id,
            suggested_by=user.id
        )
        db_session.add(suggestion)
        db_session.commit()
        db_session.refresh(suggestion)

        assert suggestion.id is not None
        assert suggestion.trip_id == trip.id
        assert suggestion.place_id == place.id
        assert suggestion.suggested_by == user.id
        assert suggestion.suggested_at is not None
        assert isinstance(suggestion.suggested_at, datetime)
        assert suggestion.status == "voting"  # Default value
        assert suggestion.votes_for == 0  # Default value
        assert suggestion.votes_against == 0  # Default value

    def test_suggestion_default_values(self, db_session):
        """Test default values for suggestion fields."""
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

        suggestion = Suggestion(
            trip_id=trip.id,
            place_id=place.id,
            suggested_by=user.id
        )
        db_session.add(suggestion)
        db_session.commit()
        db_session.refresh(suggestion)

        assert suggestion.status == "voting"
        assert suggestion.votes_for == 0
        assert suggestion.votes_against == 0

    def test_suggestion_required_fields(self, db_session):
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

        # Test missing place_id
        suggestion1 = Suggestion(
            trip_id=trip.id,
            suggested_by=user.id
        )
        db_session.add(suggestion1)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_suggestion_relationships(self, db_session):
        """Test that suggestion relationships are properly set up."""
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

        suggestion = Suggestion(
            trip_id=trip.id,
            place_id=place.id,
            suggested_by=user.id
        )
        db_session.add(suggestion)
        db_session.commit()
        db_session.refresh(suggestion)

        # Test that relationship attributes exist
        assert hasattr(suggestion, 'trip')
        assert hasattr(suggestion, 'place')
        assert hasattr(suggestion, 'suggested_by_user')
        assert hasattr(suggestion, 'votes')

    def test_suggestion_trip_relationship(self, db_session):
        """Test the relationship between suggestion and trip."""
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

        suggestion = Suggestion(
            trip_id=trip.id,
            place_id=place.id,
            suggested_by=user.id
        )
        db_session.add(suggestion)
        db_session.commit()
        db_session.refresh(suggestion)

        # Test the relationship
        assert suggestion.trip.id == trip.id
        assert suggestion.trip.title == trip.title

    def test_suggestion_place_relationship(self, db_session):
        """Test the relationship between suggestion and place."""
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

        suggestion = Suggestion(
            trip_id=trip.id,
            place_id=place.id,
            suggested_by=user.id
        )
        db_session.add(suggestion)
        db_session.commit()
        db_session.refresh(suggestion)

        # Test the relationship
        assert suggestion.place.id == place.id
        assert suggestion.place.name == place.name


class TestVote:
    """Test cases for Vote model."""

    def test_vote_creation(self, db_session):
        """Test creating a vote with valid data."""
        user = User(email="test@example.com", username="testuser")
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
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
        suggestion = Suggestion(
            trip_id=trip.id,
            place_id=place.id,
            suggested_by=user.id
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.add(place)
        db_session.add(suggestion)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)
        db_session.refresh(place)
        db_session.refresh(suggestion)

        vote = Vote(
            suggestion_id=suggestion.id,
            user_id=user.id,
            vote=True
        )
        db_session.add(vote)
        db_session.commit()
        db_session.refresh(vote)

        assert vote.id is not None
        assert vote.suggestion_id == suggestion.id
        assert vote.user_id == user.id
        assert vote.vote is True
        assert vote.voted_at is not None
        assert isinstance(vote.voted_at, datetime)

    def test_vote_relationships(self, db_session):
        """Test that vote relationships are properly set up."""
        user = User(email="test@example.com", username="testuser")
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
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
        suggestion = Suggestion(
            trip_id=trip.id,
            place_id=place.id,
            suggested_by=user.id
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.add(place)
        db_session.add(suggestion)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)
        db_session.refresh(place)
        db_session.refresh(suggestion)

        vote = Vote(
            suggestion_id=suggestion.id,
            user_id=user.id,
            vote=True
        )
        db_session.add(vote)
        db_session.commit()
        db_session.refresh(vote)

        # Test that relationship attributes exist
        assert hasattr(vote, 'suggestion')
        assert hasattr(vote, 'user')

        # Test the relationships
        assert vote.suggestion.id == suggestion.id
        assert vote.user.id == user.id
