from itertools import count

from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, Date, Time, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


_id_counter = count(1)


def reset_id_counter() -> None:
    global _id_counter
    _id_counter = count(1)


def _gen_id() -> int:
    return next(_id_counter)


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    created_time = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if getattr(self, "id", None) is None:
            self.id = _gen_id()
    
    # Relationships
    trips_admin = relationship("Trip", back_populates="admin_user", foreign_keys="Trip.admin")
    trip_members = relationship("TripMember", back_populates="user")
    expenses_paid = relationship("Expense", back_populates="paid_by_user")
    suggestions = relationship("Suggestion", back_populates="suggested_by_user")
    votes = relationship("Vote", back_populates="user")
    expense_shares = relationship("ExpenseShare", back_populates="user")
    routes_added = relationship("Route", back_populates="added_by_user")


class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    admin = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if getattr(self, "id", None) is None:
            self.id = _gen_id()
    
    # Relationships
    admin_user = relationship("User", back_populates="trips_admin", foreign_keys=[admin])
    members = relationship("TripMember", back_populates="trip", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="trip", cascade="all, delete-orphan")
    suggestions = relationship("Suggestion", back_populates="trip", cascade="all, delete-orphan")
    routes = relationship("Route", back_populates="trip", cascade="all, delete-orphan")


class TripMember(Base):
    __tablename__ = "trip_members"

    __table_args__ = (
        UniqueConstraint("trip_id", "user_id", name="uq_trip_members_trip_user"),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    role = Column(String(20), default="member")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if getattr(self, "id", None) is None:
            self.id = _gen_id()
    
    # Relationships
    trip = relationship("Trip", back_populates="members")
    user = relationship("User", back_populates="trip_members")


class Place(Base):
    __tablename__ = "places"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    lat = Column(Numeric(10, 8), nullable=False)
    lng = Column(Numeric(11, 8), nullable=False)
    osm_id = Column(String(255), unique=True)
    address = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if getattr(self, "id", None) is None:
            self.id = _gen_id()
    
    # Relationships
    suggestions = relationship("Suggestion", back_populates="place")
    routes = relationship("Route", back_populates="place")


class Suggestion(Base):
    __tablename__ = "suggestions"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    suggested_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    suggested_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="voting")
    votes_for = Column(Integer, default=0)
    votes_against = Column(Integer, default=0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if getattr(self, "id", None) is None:
            self.id = _gen_id()
    
    # Relationships
    trip = relationship("Trip", back_populates="suggestions")
    place = relationship("Place", back_populates="suggestions")
    suggested_by_user = relationship("User", back_populates="suggestions")
    votes = relationship("Vote", back_populates="suggestion", cascade="all, delete-orphan")


class Vote(Base):
    __tablename__ = "votes"
    
    id = Column(Integer, primary_key=True, index=True)
    suggestion_id = Column(Integer, ForeignKey("suggestions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vote = Column(Boolean, nullable=False)
    voted_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if getattr(self, "id", None) is None:
            self.id = _gen_id()
    
    # Relationships
    suggestion = relationship("Suggestion", back_populates="votes")
    user = relationship("User", back_populates="votes")


class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    order_in_day = Column(Integer, nullable=False)
    planned_time = Column(Time)
    estimated_cost = Column(Numeric(10, 2))
    notes = Column(Text)
    added_by = Column(Integer, ForeignKey("users.id"))
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if getattr(self, "id", None) is None:
            self.id = _gen_id()
    
    # Relationships
    trip = relationship("Trip", back_populates="routes")
    place = relationship("Place", back_populates="routes")
    added_by_user = relationship("User", back_populates="routes_added")


class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    title = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="RUB")
    paid_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if getattr(self, "id", None) is None:
            self.id = _gen_id()
    
    # Relationships
    trip = relationship("Trip", back_populates="expenses")
    paid_by_user = relationship("User", back_populates="expenses_paid")
    shares = relationship("ExpenseShare", back_populates="expense", cascade="all, delete-orphan")


class ExpenseShare(Base):
    __tablename__ = "expense_shares"
    
    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    share = Column(Numeric(3, 2), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if getattr(self, "id", None) is None:
            self.id = _gen_id()
    
    # Relationships
    expense = relationship("Expense", back_populates="shares")
    user = relationship("User", back_populates="expense_shares")
