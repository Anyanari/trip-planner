from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Place as PlaceModel
from ..schemas import Place as PlaceSchema, PlaceCreate, OSMPlace, OSMSearchResponse
from ..services.osm_service import search_places, get_place_details, search_places_sync

router = APIRouter(prefix="/api/places", tags=["places"])


@router.post("/", response_model=PlaceSchema)
def create_place(place: PlaceCreate, db: Session = Depends(get_db)):
    # Check if place with same osm_id already exists
    if place.osm_id:
        existing_place = db.query(PlaceModel).filter(PlaceModel.osm_id == place.osm_id).first()
        if existing_place:
            return existing_place
    
    db_place = PlaceModel(
        name=place.name,
        lat=place.lat,
        lng=place.lng,
        osm_id=place.osm_id,
        address=place.address
    )
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place


@router.get("/", response_model=List[PlaceSchema])
def get_places(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    places = db.query(PlaceModel).offset(skip).limit(limit).all()
    return places


@router.get("/search", response_model=OSMSearchResponse)
def search_places_endpoint(query: str, limit: int = 10):
    try:
        places = search_places_sync(query, limit)
        return OSMSearchResponse(places=places)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{place_id}", response_model=PlaceSchema)
def get_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(PlaceModel).filter(PlaceModel.id == place_id).first()
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    return place
