from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import get_db
from .routers import users, trips, places, suggestions, routes, expenses
from .config import settings
import json
from datetime import date, datetime
from decimal import Decimal
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI(
    title=settings.app_name,
    description="Trip Planner API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(trips.router)
app.include_router(places.router)
app.include_router(suggestions.router)
app.include_router(routes.router)
app.include_router(expenses.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Trip Planner API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Custom JSON response class
class CustomJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(
            content, 
            default=lambda o: o.isoformat() if isinstance(o, (date, datetime)) else format(o, "f") if isinstance(o, Decimal) else o
        ).encode("utf-8")

# Override default response class
app.default_response_class = CustomJSONResponse

# Add JSON serialization middleware
class JSONMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Override the render method for JSON responses
        if hasattr(response, 'render') and callable(response.render):
            original_render = response.render
            
            def custom_render(content):
                if isinstance(content, dict):
                    # Recursively serialize dates in dict
                    def serialize_dict(obj):
                        if isinstance(obj, dict):
                            return {k: serialize_value(v) for k, v in obj.items()}
                        elif isinstance(obj, list):
                            return [serialize_value(item) for item in obj]
                        else:
                            return serialize_value(obj)
                    
                    def serialize_value(obj):
                        if isinstance(obj, (date, datetime)):
                            return obj.isoformat()
                        elif isinstance(obj, Decimal):
                            return format(obj, "f")
                        return obj
                    
                    try:
                        # Try to parse and re-serialize
                        import json
                        content_dict = json.loads(original_render(content).decode())
                        serialized = json.dumps(serialize_dict(content_dict), default=str)
                        return serialized.encode('utf-8')
                    except:
                        return original_render(content)
                
                response.render = custom_render
        
        return response

# Add middleware to app
app.add_middleware(JSONMiddleware)
