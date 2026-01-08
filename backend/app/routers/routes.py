from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Route as RouteModel, Trip as TripModel, Place as PlaceModel, User as UserModel
from ..schemas import Route as RouteSchema, RouteCreate, RouteUpdate

router = APIRouter(prefix="/api/routes", tags=["routes"])


@router.post("/", response_model=RouteSchema)
def create_route(route: RouteCreate, db: Session = Depends(get_db)):
    # Check if trip exists
    trip = db.query(TripModel).filter(TripModel.id == route.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Check if place exists
    place = db.query(PlaceModel).filter(PlaceModel.id == route.place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    
    # Check if route already exists for this place in trip
    existing = db.query(RouteModel).filter(
        RouteModel.trip_id == route.trip_id,
        RouteModel.place_id == route.place_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Place already in route")
    
    db_route = RouteModel(
        trip_id=route.trip_id,
        place_id=route.place_id,
        day_number=route.day_number,
        order_in_day=route.order_in_day,
        planned_time=route.planned_time,
        estimated_cost=route.estimated_cost,
        notes=route.notes,
        added_by=route.added_by
    )
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route


@router.get("/trip/{trip_id}", response_model=List[RouteSchema])
def get_trip_routes(trip_id: int, db: Session = Depends(get_db)):
    routes = db.query(RouteModel).filter(RouteModel.trip_id == trip_id).order_by(
        RouteModel.day_number, RouteModel.order_in_day
    ).all()
    return routes


@router.get("/trip/{trip_id}/day/{day_number}", response_model=List[RouteSchema])
def get_day_routes(trip_id: int, day_number: int, db: Session = Depends(get_db)):
    routes = db.query(RouteModel).filter(
        RouteModel.trip_id == trip_id,
        RouteModel.day_number == day_number
    ).order_by(RouteModel.order_in_day).all()
    return routes


@router.get("/{route_id}", response_model=RouteSchema)
def get_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(RouteModel).filter(RouteModel.id == route_id).first()
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route


@router.patch("/{route_id}", response_model=RouteSchema)
def update_route(route_id: int, route_update: RouteUpdate, db: Session = Depends(get_db)):
    route = db.query(RouteModel).filter(RouteModel.id == route_id).first()
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    
    update_data = route_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(route, field, value)
    
    db.commit()
    db.refresh(route)
    return route


@router.delete("/{route_id}")
def delete_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(RouteModel).filter(RouteModel.id == route_id).first()
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    
    db.delete(route)
    db.commit()
    return {"message": "Route deleted successfully"}
