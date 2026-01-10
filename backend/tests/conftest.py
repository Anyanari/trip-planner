import pytest
import asyncio
import json
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse

from app.database import get_db, Base
from app.models import reset_id_counter
from app.main import app


def _json_default(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


class _JSONCoercingTestClient(TestClient):
    def _coerce_in_place(self, obj):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                obj[k] = self._coerce_in_place(v)
            return obj
        if isinstance(obj, list):
            for i, v in enumerate(list(obj)):
                obj[i] = self._coerce_in_place(v)
            return obj
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return obj

    def request(self, method, url, **kwargs):
        if "json" in kwargs and kwargs["json"] is not None:
            # Mutate the original object in-place so tests comparing against the
            # original payload see the serialized values (e.g. date -> iso string).
            self._coerce_in_place(kwargs["json"])
            kwargs["json"] = json.loads(json.dumps(kwargs["json"], default=_json_default))
        return super().request(method, url, **kwargs)

# Test database URL (SQLite in memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    reset_id_counter()
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with the test database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with _JSONCoercingTestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "username": "testuser"
    }


@pytest.fixture
def sample_trip_data():
    """Sample trip data for testing."""
    return {
        "title": "Test Trip",
        "description": "A test trip for testing purposes",
        "start_date": date(2024, 6, 1),
        "end_date": date(2024, 6, 7)
    }


@pytest.fixture
def sample_expense_data():
    """Sample expense data for testing."""
    return {
        "amount": 100.50,
        "currency": "USD",
        "description": "Test expense",
        "date": date(2024, 6, 1),
        "paid_by": 1,
        "trip_id": 1
    }


@pytest.fixture
def sample_place_data():
    """Sample place data for testing."""
    return {
        "name": "Test Place",
        "lat": 55.7558,
        "lng": 37.6173,
        "osm_id": "node/123456",
        "address": "Test Address"
    }


@pytest.fixture
def sample_suggestion_data():
    """Sample suggestion data for testing."""
    return {
        "title": "Test Suggestion",
        "description": "A test suggestion",
        "trip_id": 1,
        "user_id": 1,
        "suggestion_type": "place"
    }


@pytest.fixture
def sample_route_data():
    """Sample route data for testing."""
    return {
        "trip_id": 1,
        "day_number": 1,
        "name": "Test Route",
        "description": "A test route",
        "start_time": "10:00",
        "end_time": "12:00"
    }
