import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app.models import User, Trip

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    return TestClient(app)

@pytest.fixture
def test_user(db):
    user = User(email="test@example.com", username="testuser")
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

@pytest.fixture
def test_trip(db, test_user):
    trip = Trip(
        title="Test Trip",
        description="A test trip",
        start_date="2026-01-01",
        end_date="2026-01-02",
        admin=test_user.id
    )
    db = TestingSessionLocal()
    db.add(trip)
    db.commit()
    db.refresh(trip)
    db.close()
    return trip
