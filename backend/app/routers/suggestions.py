from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import (
    Suggestion as SuggestionModel, Vote as VoteModel,
    Trip as TripModel, Place as PlaceModel, User as UserModel
)
from ..schemas import (
    Suggestion as SuggestionSchema, SuggestionCreate,
    Vote as VoteSchema, VoteCreate
)

router = APIRouter(prefix="/api/suggestions", tags=["suggestions"])


@router.post("/", response_model=SuggestionSchema)
def create_suggestion(suggestion: SuggestionCreate, db: Session = Depends(get_db)):
    # Check if trip exists
    trip = db.query(TripModel).filter(TripModel.id == suggestion.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Check if place exists
    place = db.query(PlaceModel).filter(PlaceModel.id == suggestion.place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    
    # Check if suggestion already exists
    existing = db.query(SuggestionModel).filter(
        SuggestionModel.trip_id == suggestion.trip_id,
        SuggestionModel.place_id == suggestion.place_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Suggestion already exists")
    
    db_suggestion = SuggestionModel(
        trip_id=suggestion.trip_id,
        place_id=suggestion.place_id,
        suggested_by=suggestion.trip_id  # This should be user_id, fix in implementation
    )
    db.add(db_suggestion)
    db.commit()
    db.refresh(db_suggestion)
    return db_suggestion


@router.post("/trip/{trip_id}", response_model=SuggestionSchema)
def suggest_place_for_trip(
    trip_id: int, place_id: int, suggested_by: int, db: Session = Depends(get_db)
):
    # Check if trip exists
    trip = db.query(TripModel).filter(TripModel.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Check if place exists
    place = db.query(PlaceModel).filter(PlaceModel.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    
    # Check if suggestion already exists
    existing = db.query(SuggestionModel).filter(
        SuggestionModel.trip_id == trip_id,
        SuggestionModel.place_id == place_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Suggestion already exists")
    
    db_suggestion = SuggestionModel(
        trip_id=trip_id,
        place_id=place_id,
        suggested_by=suggested_by
    )
    db.add(db_suggestion)
    db.commit()
    db.refresh(db_suggestion)
    return db_suggestion


@router.get("/trip/{trip_id}", response_model=List[SuggestionSchema])
def get_trip_suggestions(trip_id: int, db: Session = Depends(get_db)):
    suggestions = db.query(SuggestionModel).filter(
        SuggestionModel.trip_id == trip_id
    ).all()
    return suggestions


@router.get("/{suggestion_id}", response_model=SuggestionSchema)
def get_suggestion(suggestion_id: int, db: Session = Depends(get_db)):
    suggestion = db.query(SuggestionModel).filter(SuggestionModel.id == suggestion_id).first()
    if suggestion is None:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    return suggestion


@router.post("/{suggestion_id}/vote", response_model=VoteSchema)
def vote_on_suggestion(
    suggestion_id: int, user_id: int, vote: VoteCreate, db: Session = Depends(get_db)
):
    # Check if suggestion exists and is in voting status
    suggestion = db.query(SuggestionModel).filter(SuggestionModel.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    
    if suggestion.status != "voting":
        raise HTTPException(status_code=400, detail="Voting is closed for this suggestion")
    
    # Check if user is trip member
    is_member = db.query(TripModel).join(TripModel.members).filter(
        TripModel.id == suggestion.trip_id,
        TripModel.members.any(user_id=user_id)
    ).first()
    if not is_member:
        raise HTTPException(status_code=403, detail="User is not a member of this trip")
    
    # Create or update vote
    existing_vote = db.query(VoteModel).filter(
        VoteModel.suggestion_id == suggestion_id,
        VoteModel.user_id == user_id
    ).first()
    
    if existing_vote:
        existing_vote.vote = vote.vote
        db.commit()
        db.refresh(existing_vote)
        return existing_vote
    else:
        db_vote = VoteModel(
            suggestion_id=suggestion_id,
            user_id=user_id,
            vote=vote.vote
        )
        db.add(db_vote)
        db.commit()
        db.refresh(db_vote)
        return db_vote


@router.patch("/{suggestion_id}/status")
def update_suggestion_status(
    suggestion_id: int, status: str, db: Session = Depends(get_db)
):
    if status not in ["voting", "accepted", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    suggestion = db.query(SuggestionModel).filter(SuggestionModel.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    
    suggestion.status = status
    db.commit()
    db.refresh(suggestion)
    return {"message": f"Suggestion status updated to {status}"}
