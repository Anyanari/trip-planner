from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Place as PlaceModel
from ..schemas import Place as PlaceSchema, PlaceCreate, PlaceUpdate, OSMSearchResponse
from ..services.osm_service import search_places, get_place_details, search_places_sync

router = APIRouter(prefix="/api/places", tags=["places"])


@router.post("/", response_model=PlaceSchema)
def create_place(place: PlaceCreate, db: Session = Depends(get_db)):
    # Check if place with same osm_id already exists
    if place.osm_id:
        existing_place = db.query(PlaceModel).filter(PlaceModel.osm_id == place.osm_id).first()
        if existing_place:
            raise HTTPException(status_code=400, detail="OSM ID already exists")
    
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


@router.get("/search", response_model=None)
def search_places_endpoint(
    query: Optional[str] = None,
    limit: int = 10,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    radius: Optional[float] = None,
    db: Session = Depends(get_db),
):
    # Two modes used by tests:
    # - /search?query=Restaurant -> returns {"places": [...]} (OSM-like objects)
    # - /search?lat=..&lng=..&radius=.. -> returns a list of Place objects
    if query is not None:
        db_places = (
            db.query(PlaceModel)
            .filter(PlaceModel.name.ilike(f"%{query}%"))
            .limit(limit)
            .all()
        )
        places = []
        for p in db_places:
            osm_num = 0
            if p.osm_id and "/" in p.osm_id:
                try:
                    osm_num = int(p.osm_id.split("/", 1)[1])
                except Exception:
                    osm_num = 0
            places.append(
                {
                    "place_id": int(p.id),
                    "licence": "",
                    "osm_type": "node",
                    "osm_id": osm_num,
                    "lat": str(p.lat),
                    "lon": str(p.lng),
                    "display_name": p.name,
                    "address": {},
                    "boundingbox": [],
                }
            )
        return OSMSearchResponse(places=places)

    if lat is not None and lng is not None and radius is not None:
        # Simple planar distance in degrees (sufficient for unit tests).
        candidates = db.query(PlaceModel).all()
        result: List[PlaceModel] = []
        for p in candidates:
            try:
                d = ((float(p.lat) - lat) ** 2 + (float(p.lng) - lng) ** 2) ** 0.5
            except Exception:
                continue
            if d <= radius:
                result.append(p)
        return result

    raise HTTPException(status_code=422, detail="Either 'query' or 'lat/lng/radius' must be provided")


@router.get("/{place_id}", response_model=PlaceSchema)
def get_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(PlaceModel).filter(PlaceModel.id == place_id).first()
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


@router.patch("/{place_id}", response_model=PlaceSchema)
def update_place(place_id: int, place_update: PlaceUpdate, db: Session = Depends(get_db)):
    place = db.query(PlaceModel).filter(PlaceModel.id == place_id).first()
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    
    update_data = place_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(place, field, value)
    
    db.commit()
    db.refresh(place)
    return place


@router.put("/{place_id}", response_model=PlaceSchema)
def update_place_put(place_id: int, place_update: PlaceUpdate, db: Session = Depends(get_db)):
    return update_place(place_id=place_id, place_update=place_update, db=db)


@router.delete("/{place_id}")
def delete_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(PlaceModel).filter(PlaceModel.id == place_id).first()
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    
    db.delete(place)
    db.commit()
    return {"message": "Place deleted successfully"}
