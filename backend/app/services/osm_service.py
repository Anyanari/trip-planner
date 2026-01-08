import httpx
from typing import List, Dict, Any
from ..schemas import OSMPlace


async def search_places(query: str, limit: int = 10) -> List[OSMPlace]:
    """Search places using OpenStreetMap Nominatim API"""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "addressdetails": 1,
        "limit": limit
    }
    
    headers = {
        "User-Agent": "TripPlanner/1.0 (+https://github.com/example/tripplanner)",
        "Accept": "application/json",
        "Referer": "https://github.com/example/tripplanner"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
    
    places = []
    for item in data:
        place = OSMPlace(
            place_id=item.get("place_id"),
            licence=item.get("licence"),
            osm_type=item.get("osm_type"),
            osm_id=item.get("osm_id"),
            lat=item.get("lat"),
            lon=item.get("lon"),
            display_name=item.get("display_name"),
            address=item.get("address", {}),
            boundingbox=item.get("boundingbox", [])
        )
        places.append(place)
    
    return places


def search_places_sync(query: str, limit: int = 10) -> List[OSMPlace]:
    """Synchronous version of search_places for FastAPI compatibility"""
    import asyncio
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(search_places(query, limit))
    finally:
        loop.close()


async def get_place_details(osm_id: str, osm_type: str) -> Dict[str, Any]:
    """Get detailed information about a place"""
    url = f"https://nominatim.openstreetmap.org/lookup"
    params = {
        "osm_ids": f"{osm_type}{osm_id}",
        "format": "json",
        "addressdetails": 1
    }
    
    headers = {
        "User-Agent": "TripPlanner/1.0 (+https://github.com/example/tripplanner)",
        "Accept": "application/json",
        "Referer": "https://github.com/example/tripplanner"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
    
    return data[0] if data else {}


def get_place_details_sync(osm_id: str, osm_type: str) -> Dict[str, Any]:
    """Synchronous version of get_place_details"""
    import asyncio
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(get_place_details(osm_id, osm_type))
    finally:
        loop.close()
