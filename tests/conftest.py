import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities as original_activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to original state before each test."""
    import src.app
    src.app.activities = copy.deepcopy(original_activities)
    yield
    src.app.activities = copy.deepcopy(original_activities)


@pytest.fixture
def client():
    """Create a TestClient for testing."""
    return TestClient(app)