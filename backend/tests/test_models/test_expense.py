import pytest
from decimal import Decimal
from datetime import datetime, date
from app.models import User, Trip, Expense, ExpenseShare


class TestExpense:
    """Test cases for Expense model."""

    def test_expense_creation(self, db_session):
        """Test creating an expense with valid data."""
        # Create user and trip first
        user = User(email="test@example.com", username="testuser")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=user.id
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)

        expense = Expense(
            trip_id=trip.id,
            title="Dinner at Restaurant",
            amount=Decimal('150.50'),
            currency="RUB",
            paid_by=user.id,
            date=date(2024, 6, 1)
        )
        db_session.add(expense)
        db_session.commit()
        db_session.refresh(expense)

        assert expense.id is not None
        assert expense.trip_id == trip.id
        assert expense.title == "Dinner at Restaurant"
        assert expense.amount == Decimal('150.50')
        assert expense.currency == "RUB"
        assert expense.paid_by == user.id
        assert expense.created_at is not None
        assert isinstance(expense.created_at, datetime)

    def test_expense_default_currency(self, db_session):
        """Test that currency defaults to RUB."""
        user = User(email="test@example.com", username="testuser")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=user.id
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)

        expense = Expense(
            trip_id=trip.id,
            title="Lunch",
            amount=Decimal('50.00'),
            paid_by=user.id,
            date=date(2024, 6, 2)
        )
        db_session.add(expense)
        db_session.commit()
        db_session.refresh(expense)

        assert expense.currency == "RUB"

    def test_expense_required_fields(self, db_session):
        """Test that required fields are enforced."""
        user = User(email="test@example.com", username="testuser")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=user.id
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)

        # Test missing trip_id
        expense = Expense(
            title="Test Expense",
            amount=Decimal('100.00'),
            paid_by=user.id,
            date=date(2024, 6, 1)
        )
        db_session.add(expense)
        with pytest.raises(Exception):  # Should raise an integrity error
            db_session.commit()

    def test_expense_relationships(self, db_session):
        """Test expense relationships with trip and user."""
        user = User(email="test@example.com", username="testuser")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=user.id
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)

        expense = Expense(
            trip_id=trip.id,
            title="Test Expense",
            amount=Decimal('100.00'),
            paid_by=user.id,
            date=date(2024, 6, 1)
        )
        db_session.add(expense)
        db_session.commit()
        db_session.refresh(expense)

        assert expense.trip == trip
        assert expense.paid_by_user == user

    def test_expense_trip_relationship(self, db_session):
        """Test that expense is properly linked to trip."""
        user = User(email="test@example.com", username="testuser")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=user.id
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)

        expense = Expense(
            trip_id=trip.id,
            title="Test Expense",
            amount=Decimal('100.00'),
            paid_by=user.id,
            date=date(2024, 6, 1)
        )
        db_session.add(expense)
        db_session.commit()
        db_session.refresh(expense)

        # Check that expense appears in trip's expenses
        assert expense in trip.expenses

    def test_expense_paid_by_user_relationship(self, db_session):
        """Test that expense is properly linked to paying user."""
        user = User(email="test@example.com", username="testuser")
        trip = Trip(
            title="Test Trip",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 7),
            admin=user.id
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)

        expense = Expense(
            trip_id=trip.id,
            title="Test Expense",
            amount=Decimal('100.00'),
            paid_by=user.id,
            date=date(2024, 6, 1)
        )
        db_session.add(expense)
        db_session.commit()
        db_session.refresh(expense)

        # Check that expense appears in user's paid expenses
        assert expense in user.expenses_paid


class TestExpenseShare:
    """Test cases for ExpenseShare model."""

    def test_expense_share_creation(self, db_session):
        """Test creating an expense share with valid data."""
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
        expense = Expense(
            trip_id=trip.id,
            title="Test Expense",
            amount=Decimal('100.00'),
            paid_by=user.id,
            date=date(2024, 6, 1)
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.add(expense)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)
        db_session.refresh(expense)

        expense_share = ExpenseShare(
            expense_id=expense.id,
            user_id=user.id,
            share=Decimal('0.50')
        )
        db_session.add(expense_share)
        db_session.commit()
        db_session.refresh(expense_share)

        assert expense_share.id is not None
        assert expense_share.expense_id == expense.id
        assert expense_share.user_id == user.id
        assert expense_share.share == Decimal('0.50')

    def test_expense_share_relationships(self, db_session):
        """Test that expense share relationships are properly set up."""
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
        expense = Expense(
            trip_id=trip.id,
            title="Test Expense",
            amount=Decimal('100.00'),
            paid_by=user.id,
            date=date(2024, 6, 1)
        )
        db_session.add(user)
        db_session.add(trip)
        db_session.add(expense)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(trip)
        db_session.refresh(expense)

        expense_share = ExpenseShare(
            expense_id=expense.id,
            user_id=user.id,
            share=Decimal('0.50')
        )
        db_session.add(expense_share)
        db_session.commit()
        db_session.refresh(expense_share)

        # Test that relationship attributes exist
        assert hasattr(expense_share, 'expense')
        assert hasattr(expense_share, 'user')

        # Test relationships
        assert expense_share.expense.id == expense.id
        assert expense_share.user.id == user.id
