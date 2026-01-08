from pydantic import BaseModel, EmailStr
from typing import Optional, List, Literal
from datetime import date, datetime, time


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_time: datetime
    
    class Config:
        from_attributes = True


# Trip schemas
class TripBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: date
    end_date: date


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class Trip(TripBase):
    id: int
    admin: Optional[int] = None
    created_time: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


class TripWithDetails(Trip):
    admin_user: Optional[User] = None
    members: List[User] = []


# TripMember schemas
class TripMemberBase(BaseModel):
    role: Literal["admin", "member"] = "member"


class TripMemberCreate(TripMemberBase):
    user_id: int


class TripMember(TripMemberBase):
    id: int
    trip_id: int
    user_id: int
    joined_at: datetime
    user: User
    
    class Config:
        from_attributes = True


# Place schemas
class PlaceBase(BaseModel):
    name: str
    lat: float
    lng: float
    osm_id: Optional[str] = None
    address: Optional[str] = None


class PlaceCreate(PlaceBase):
    pass


class Place(PlaceBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Suggestion schemas
class SuggestionBase(BaseModel):
    trip_id: int
    place_id: int


class SuggestionCreate(SuggestionBase):
    pass


class Suggestion(SuggestionBase):
    id: int
    suggested_by: int
    suggested_at: datetime
    status: Literal["voting", "accepted", "rejected"]
    votes_for: int
    votes_against: int
    place: Place
    suggested_by_user: User
    
    class Config:
        from_attributes = True


# Vote schemas
class VoteCreate(BaseModel):
    vote: bool


class Vote(BaseModel):
    id: int
    suggestion_id: int
    user_id: int
    vote: bool
    voted_at: datetime
    
    class Config:
        from_attributes = True


# Route schemas
class RouteBase(BaseModel):
    trip_id: int
    place_id: int
    day_number: int
    order_in_day: int
    planned_time: Optional[time] = None
    estimated_cost: Optional[float] = None
    notes: Optional[str] = None


class RouteCreate(RouteBase):
    added_by: int


class RouteUpdate(BaseModel):
    day_number: Optional[int] = None
    order_in_day: Optional[int] = None
    planned_time: Optional[time] = None
    estimated_cost: Optional[float] = None
    notes: Optional[str] = None


class Route(RouteBase):
    id: int
    added_by: Optional[int] = None
    added_at: datetime
    place: Place
    added_by_user: Optional[User] = None
    
    class Config:
        from_attributes = True


# Expense schemas
class ExpenseBase(BaseModel):
    trip_id: int
    title: str
    amount: float
    currency: str = "RUB"
    paid_by: int


class ExpenseCreate(ExpenseBase):
    shares: List[dict]  # [{"user_id": int, "share": float}]


class Expense(ExpenseBase):
    id: int
    created_at: datetime
    paid_by_user: User
    
    class Config:
        from_attributes = True


class ExpenseShareBase(BaseModel):
    expense_id: int
    user_id: int
    share: float


class ExpenseShare(ExpenseShareBase):
    id: int
    user: User
    
    class Config:
        from_attributes = True


# Balance schemas
class Balance(BaseModel):
    debtor_id: int
    debtor_name: str
    creditor_id: int
    creditor_name: str
    amount: float


# OSM Search schemas
class OSMPlace(BaseModel):
    place_id: int
    licence: str
    osm_type: str
    osm_id: int
    lat: str
    lon: str
    display_name: str
    address: dict
    boundingbox: List[str]


class OSMSearchResponse(BaseModel):
    places: List[OSMPlace]


# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
