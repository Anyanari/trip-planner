from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Trip as TripModel, User as UserModel, TripMember as TripMemberModel
from ..schemas import Trip as TripSchema, TripCreate, TripUpdate, TripWithDetails, TripMember as TripMemberSchema, TripMemberCreate

router = APIRouter(prefix="/api/trips", tags=["trips"])


@router.post("/", response_model=TripSchema)
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    # Prefer admin from request if provided; fallback to 1.
    user_id = trip.admin or 1

    admin_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not admin_user:
        raise HTTPException(status_code=400, detail="Admin user not found")
    
    # Create trip with specified user as admin
    db_trip = TripModel(
        title=trip.title,
        description=trip.description,
        start_date=trip.start_date,
        end_date=trip.end_date,
        admin=user_id
    )
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    
    # Add user as admin member
    db_member = TripMemberModel(trip_id=db_trip.id, user_id=user_id)
    db.add(db_member)
    db.commit()
    
    return db_trip


@router.get("/", response_model=List[TripSchema])
def get_trips(
    skip: int = 0, 
    limit: int = 100, 
    admin_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(TripModel)
    if admin_id is not None:
        query = query.filter(TripModel.admin == admin_id)
    trips = query.offset(skip).limit(limit).all()
    return trips


@router.get("/{trip_id}", response_model=TripWithDetails)
def get_trip(
    trip_id: int, 
    db: Session = Depends(get_db)
):
    # Check if trip exists
    trip = db.query(TripModel).filter(TripModel.id == trip_id).first()
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Get members
    members = db.query(UserModel).join(TripMemberModel, UserModel.id == TripMemberModel.user_id).filter(
        TripMemberModel.trip_id == trip_id
    ).all()
    
    return TripWithDetails(
        **trip.__dict__,
        admin_user=trip.admin_user,
        members=members
    )


@router.patch("/{trip_id}", response_model=TripSchema)
def update_trip(trip_id: int, trip_update: TripUpdate, db: Session = Depends(get_db)):
    trip = db.query(TripModel).filter(TripModel.id == trip_id).first()
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    update_data = trip_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(trip, field, value)
    
    db.commit()
    db.refresh(trip)
    return trip


@router.put("/{trip_id}", response_model=TripSchema)
def update_trip_put(trip_id: int, trip_update: TripUpdate, db: Session = Depends(get_db)):
    return update_trip(trip_id=trip_id, trip_update=trip_update, db=db)


@router.delete("/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(TripModel).filter(TripModel.id == trip_id).first()
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Полностью удаляем поездку из базы
    db.delete(trip)
    db.commit()
    return {"message": "Trip deleted successfully"}


@router.post("/{trip_id}/members", response_model=TripMemberSchema)
def add_trip_member(trip_id: int, member: TripMemberCreate, db: Session = Depends(get_db)):
    # Check if trip exists
    trip = db.query(TripModel).filter(TripModel.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Check if user exists
    user = db.query(UserModel).filter(UserModel.id == member.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user is already a member
    existing_member = db.query(TripMemberModel).filter(
        TripMemberModel.trip_id == trip_id,
        TripMemberModel.user_id == member.user_id
    ).first()
    if existing_member:
        raise HTTPException(status_code=400, detail="User is already a member")
    
    db_member = TripMemberModel(
        trip_id=trip_id,
        user_id=member.user_id
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.get("/{trip_id}/members", response_model=List[TripMemberSchema])
def get_trip_members(trip_id: int, db: Session = Depends(get_db)):
    members = db.query(TripMemberModel).filter(TripMemberModel.trip_id == trip_id).all()
    return members


@router.delete("/{trip_id}/members/{user_id}")
def remove_trip_member(trip_id: int, user_id: int, db: Session = Depends(get_db)):
    member = db.query(TripMemberModel).filter(
        TripMemberModel.trip_id == trip_id,
        TripMemberModel.user_id == user_id
    ).first()
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    
    db.delete(member)
    db.commit()
    return {"message": "Member removed successfully"}
