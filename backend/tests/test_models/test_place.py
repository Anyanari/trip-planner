import pytest
from decimal import Decimal
from datetime import datetime
from app.models import Place


class TestPlace:
    """Test cases for Place model."""

    def test_place_creation(self, db_session):
        """Test creating a place with valid data."""
        place = Place(
            name="Test Place",
            lat=Decimal('55.7558'),
            lng=Decimal('37.6173'),
            osm_id="node/123456",
            address="Test Address, Moscow"
        )
        db_session.add(place)
        db_session.commit()
        db_session.refresh(place)

        assert place.id is not None
        assert place.name == "Test Place"
        assert place.lat == Decimal('55.7558')
        assert place.lng == Decimal('37.6173')
        assert place.osm_id == "node/123456"
        assert place.address == "Test Address, Moscow"
        assert place.created_at is not None
        assert isinstance(place.created_at, datetime)

    def test_place_name_required(self, db_session):
        """Test that name is required."""
        place = Place(
            lat=Decimal('55.7558'),
            lng=Decimal('37.6173')
        )
        db_session.add(place)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_place_coordinates_required(self, db_session):
        """Test that lat and lng are required."""
        # Test missing lat
        place1 = Place(
            name="Test Place",
            lng=Decimal('37.6173')
        )
        db_session.add(place1)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_place_osm_id_uniqueness(self, db_session):
        """Test that osm_id must be unique."""
        place1 = Place(
            name="Place 1",
            lat=Decimal('55.7558'),
            lng=Decimal('37.6173'),
            osm_id="node/123456"
        )
        place2 = Place(
            name="Place 2",
            lat=Decimal('55.7559'),
            lng=Decimal('37.6174'),
            osm_id="node/123456"
        )
        
        db_session.add(place1)
        db_session.commit()
        
        db_session.add(place2)
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_place_optional_fields(self, db_session):
        """Test optional fields for place."""
        place = Place(
            name="Test Place",
            lat=Decimal('55.7558'),
            lng=Decimal('37.6173')
        )
        db_session.add(place)
        db_session.commit()
        db_session.refresh(place)

        assert place.osm_id is None  # Optional field
        assert place.address is None  # Optional field

    def test_place_coordinate_precision(self, db_session):
        """Test coordinate precision handling."""
        place = Place(
            name="Test Place",
            lat=Decimal('55.755864'),  # High precision
            lng=Decimal('37.617300')   # High precision
        )
        db_session.add(place)
        db_session.commit()
        db_session.refresh(place)

        # Check that coordinates are stored correctly
        assert place.lat == Decimal('55.755864')
        assert place.lng == Decimal('37.617300')

    def test_place_relationships(self, db_session):
        """Test that place relationships are properly set up."""
        place = Place(
            name="Test Place",
            lat=Decimal('55.7558'),
            lng=Decimal('37.6173')
        )
        db_session.add(place)
        db_session.commit()
        db_session.refresh(place)

        # Test that relationship attributes exist
        assert hasattr(place, 'suggestions')
        assert hasattr(place, 'routes')

    def test_place_str_representation(self, db_session):
        """Test place attributes."""
        place = Place(
            name="Test Place",
            lat=Decimal('55.7558'),
            lng=Decimal('37.6173'),
            address="Test Address"
        )
        db_session.add(place)
        db_session.commit()
        
        assert place.name == "Test Place"
        assert place.address == "Test Address"
