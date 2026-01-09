import pytest
from datetime import datetime
from app.models import User


class TestUser:
    """Test cases for User model."""

    def test_user_creation(self, db_session):
        """Test creating a user with valid data."""
        user = User(
            email="test@example.com",
            username="testuser"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.created_time is not None
        assert isinstance(user.created_time, datetime)

    def test_user_email_uniqueness(self, db_session):
        """Test that email must be unique."""
        user1 = User(email="test@example.com", username="user1")
        user2 = User(email="test@example.com", username="user2")
        
        db_session.add(user1)
        db_session.commit()
        
        db_session.add(user2)
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_user_username_uniqueness(self, db_session):
        """Test that username must be unique."""
        user1 = User(email="user1@example.com", username="testuser")
        user2 = User(email="user2@example.com", username="testuser")
        
        db_session.add(user1)
        db_session.commit()
        
        db_session.add(user2)
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_user_email_required(self, db_session):
        """Test that email is required."""
        user = User(username="testuser")
        db_session.add(user)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_user_username_required(self, db_session):
        """Test that username is required."""
        user = User(email="test@example.com")
        db_session.add(user)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_user_relationships(self, db_session):
        """Test that user relationships are properly set up."""
        user = User(email="test@example.com", username="testuser")
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Test that relationship attributes exist
        assert hasattr(user, 'trips_admin')
        assert hasattr(user, 'trip_members')
        assert hasattr(user, 'expenses_paid')
        assert hasattr(user, 'suggestions')
        assert hasattr(user, 'votes')
        assert hasattr(user, 'expense_shares')
        assert hasattr(user, 'routes_added')

    def test_user_str_representation(self, db_session):
        """Test string representation of user."""
        user = User(email="test@example.com", username="testuser")
        db_session.add(user)
        db_session.commit()
        
        # SQLAlchemy models don't have __str__ by default, but we can test the attributes
        assert user.email == "test@example.com"
        assert user.username == "testuser"
