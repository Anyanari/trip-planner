from pydantic import BaseModel, EmailStr
from typing import Optional, List, Literal
import datetime as dt
from decimal import Decimal


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_time: dt.datetime
    
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_time: dt.datetime
    
    class Config:
        from_attributes = True


# Trip schemas
class TripBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: dt.date
    end_date: dt.date


class TripCreate(TripBase):
    admin: Optional[int] = None


class TripUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[dt.date] = None
    end_date: Optional[dt.date] = None


class Trip(TripBase):
    id: int
    admin: Optional[int] = None
    created_time: dt.datetime
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
    joined_at: dt.datetime
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


class PlaceUpdate(BaseModel):
    name: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    osm_id: Optional[str] = None
    address: Optional[str] = None


class Place(PlaceBase):
    id: int
    created_at: dt.datetime
    
    class Config:
        from_attributes = True


# Suggestion schemas
class SuggestionBase(BaseModel):
    trip_id: int
    place_id: int


class SuggestionCreate(SuggestionBase):
    suggested_by: int
    suggestion_type: str = "place"


class Suggestion(SuggestionBase):
    id: int
    suggested_by: int
    suggested_at: dt.datetime
    status: str
    votes_for: int
    votes_against: int
    place: Optional[Place] = None
    suggested_by_user: Optional[User] = None
    
    class Config:
        from_attributes = True


# Vote schemas
class VoteCreate(BaseModel):
    vote: bool


class VoteRequest(BaseModel):
    user_id: int
    vote: bool


class Vote(BaseModel):
    id: int
    suggestion_id: int
    user_id: int
    vote: bool
    voted_at: dt.datetime
    
    class Config:
        from_attributes = True


# Route schemas
class RouteBase(BaseModel):
    trip_id: int
    place_id: int
    day_number: int
    order_in_day: int
    planned_time: Optional[dt.time] = None
    estimated_cost: Optional[Decimal] = None
    notes: Optional[str] = None


class RouteCreate(RouteBase):
    added_by: Optional[int] = None


class RouteUpdate(BaseModel):
    day_number: Optional[int] = None
    order_in_day: Optional[int] = None
    planned_time: Optional[dt.time] = None
    estimated_cost: Optional[Decimal] = None
    notes: Optional[str] = None


class Route(RouteBase):
    id: int
    added_by: Optional[int] = None
    added_at: dt.datetime
    place: Optional[Place] = None
    added_by_user: Optional[User] = None
    
    class Config:
        from_attributes = True


# Expense schemas
class ExpenseBase(BaseModel):
    trip_id: int
    title: str
    amount: Decimal
    currency: str = "RUB"
    paid_by: int
    date: Optional[dt.date] = None


class ExpenseShareCreate(BaseModel):
    user_id: int
    share: float


class ExpenseCreate(ExpenseBase):
    shares: Optional[List[ExpenseShareCreate]] = None


class Expense(ExpenseBase):
    id: int
    created_at: dt.datetime
    paid_by_user: Optional[User] = None
    
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


class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[Decimal] = None
    currency: Optional[str] = None
    paid_by: Optional[int] = None
    date: Optional[dt.date] = None


class SuggestionUpdate(BaseModel):
    status: Optional[str] = None
