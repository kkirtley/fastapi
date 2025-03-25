"""Test cases for user-related API endpoints."""

import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.main import app
from app.api.v1.routes.users import update_user, create_user, get_user, delete_user


# client = TestClient(app) # unneeded unless integration tests are implemented


@pytest.fixture
def mock_db(mocker):
    """Fixture to create a mock database session."""
    return mocker.MagicMock(spec=Session)


def test_create_user_success(mock_db, mocker) -> None:
    """Test the successful creation of a new user."""
    # Prepare test data
    new_user_data = {"name": "New User", "email": "newuser@example.com"}
    user_create = UserCreate(**new_user_data)
    mock_user = User(id=1, **new_user_data)

    # Mock the database methods
    # Simulate no existing user
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.add = mocker.MagicMock()  # Mock the add method
    mock_db.commit = mocker.MagicMock()  # Mock the commit method
    mock_db.refresh = mocker.MagicMock(side_effect=lambda user: setattr(
        user, "id", 1))  # Simulate setting the ID

    # Call the create_user function
    response = create_user(user=user_create, db=mock_db)
    validate_user = UserResponse.model_validate(
        mock_user)  # Validate the response

    # Assert the response
    assert response.id == validate_user.id
    assert response.name == validate_user.name
    assert response.email == validate_user.email

    # Verify that the mocked methods were called
    args, _ = mock_db.add.call_args
    added_user = args[0]
    assert isinstance(added_user, User)
    assert added_user.name == new_user_data["name"]
    assert added_user.email == new_user_data["email"]


def test_create_user_duplicate_email(mock_db) -> None:
    """Test creating a user with an email that already exists."""
    existing_user = User(id=1, name="Existing User",
                         email="existing@example.com")
    user_create = UserCreate(name="New User", email="existing@example.com")

    # Mock the query to simulate an existing user
    mock_db.query.return_value.filter.return_value.first.return_value = existing_user

    # Call the create_user function and assert the exception
    with pytest.raises(HTTPException) as exc_info:
        create_user(user=user_create, db=mock_db)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Email already in use"


def test_get_user_success(mock_db) -> None:
    """Test the successful retrieval of a user by ID."""
    mock_user = User(id=1, name="Test User", email="test@example.com")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    # Call the get_user function
    response = get_user(user_id=1, db=mock_db)
    validate_user = UserResponse.model_validate(mock_user)
    # Assert the response
    assert response == validate_user


def test_get_user_not_found(mock_db) -> None:
    """Test the retrieval of a user by ID that does not exist."""
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Call the get_user function and assert the exception
    with pytest.raises(HTTPException) as exc_info:
        get_user(user_id=1, db=mock_db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


def test_update_user_success(mock_db, mocker) -> None:
    """Test the successful update of a user's information."""
    mock_user = User(id=1, name="Old Name", email="old@example.com")
    updated_data = {"name": "New Name", "email": "new@example.com"}
    user_update = UserUpdate(**updated_data)
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    # Mock the commit and refresh methods
    mock_db.commit = mocker.MagicMock()
    mock_db.refresh = mocker.MagicMock()

    # Call the update_user function
    response = update_user(user_id=1, user=user_update, db=mock_db)

    # Assert the response
    assert response.name == updated_data["name"]
    assert response.email == updated_data["email"]

    # Verify that the mocked methods were called
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_user)


def test_update_user_not_found(mock_db) -> None:
    """Test updating a user that does not exist."""
    updated_data = {"name": "New Name", "email": "new@example.com"}
    user_update = UserUpdate(**updated_data)
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Call the update_user function and assert the exception
    with pytest.raises(HTTPException) as exc_info:
        update_user(user_id=1, user=user_update, db=mock_db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


def test_delete_user_success(mock_db, mocker) -> None:
    """Test the successful deletion of a user."""
    mock_user = User(id=1, name="Test User", email="test@example.com")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    # Mock the delete and commit methods
    mock_db.delete = mocker.MagicMock()
    mock_db.commit = mocker.MagicMock()

    # Call the delete_user function
    response = delete_user(user_id=1, db=mock_db)

    # Assert the response
    assert response == {"detail": "User deleted successfully"}

    # Verify that the mocked methods were called
    mock_db.delete.assert_called_once_with(mock_user)
    mock_db.commit.assert_called_once()


def test_delete_user_not_found(mock_db) -> None:
    """Test deleting a user that does not exist."""
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Call the delete_user function and assert the exception
    with pytest.raises(HTTPException) as exc_info:
        delete_user(user_id=1, db=mock_db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"
