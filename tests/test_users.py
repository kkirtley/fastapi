""" Test cases for user-related API endpoints."""
import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.api.v1.routes.users import get_user
from app.models.user import User
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_db(mocker):
    """Fixture to create a mock database session."""
    return mocker.Mock(spec=Session)

def test_get_user_success(mock_db):
    """Test the successful retrieval of a user by ID."""
    mock_user = User(id=1, name="Test User", email="test@example.com")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    # Call the get_user function
    response = get_user(user_id=1, db=mock_db)

    # Assert the response
    assert response == mock_user

def test_get_user_not_found(mock_db):
    """ Mock the database session and user query """
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Call the get_user function and assert the exception
    with pytest.raises(HTTPException) as exc_info:
        get_user(user_id=1, db=mock_db)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"

