from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import get_db
from .routers import users, trips, places, suggestions, routes, expenses
from .config import settings

app = FastAPI(
    title=settings.app_name,
    description="Trip Planner API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
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
