"""Test cases for user-related API endpoints.

This file contains unit tests for user-related API endpoints in a FastAPI application.
It uses mock objects to simulate database interactions and validate the behavior of
the application without requiring a real database connection.

For integration tests, you can use FastAPI's TestClient to test the actual API endpoints.
"""

import pytest
from sqlalchemy.orm import Session
# from fastapi.testclient import TestClient  # Uncomment for integration tests
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
# from app.main import app  # Uncomment for integration tests
from app.api.v1.routes.users import update_user, create_user, get_user, delete_user


# client = TestClient(app)  # Uncomment if you want to implement integration tests


@pytest.fixture
def mock_db(mocker):
    """Fixture to create a mock database session.

    This fixture uses the `mocker` library to create a mock object that simulates
    a SQLAlchemy database session. It is used to test database interactions without
    requiring a real database connection.
    """
    return mocker.MagicMock(spec=Session)


def test_create_user_success(mock_db, mocker) -> None:
    """Test the successful creation of a new user.

    This test validates that the `create_user` function correctly adds a new user
    to the database and returns the expected response.
    """
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
    """Test creating a user with an email that already exists.

    This test ensures that the `create_user` function raises an HTTPException
    when attempting to create a user with a duplicate email.
    """
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
    """Test the successful retrieval of a user by ID.

    This test validates that the `get_user` function correctly retrieves a user
    from the database when the user exists.
    """
    mock_user = User(id=1, name="Test User", email="test@example.com")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    # Call the get_user function
    response = get_user(user_id=1, db=mock_db)
    validate_user = UserResponse.model_validate(mock_user)
    # Assert the response
    assert response == validate_user


def test_get_user_not_found(mock_db) -> None:
    """Test the retrieval of a user by ID that does not exist.

    This test ensures that the `get_user` function raises an HTTPException
    when the user is not found in the database.
    """
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Call the get_user function and assert the exception
    with pytest.raises(HTTPException) as exc_info:
        get_user(user_id=1, db=mock_db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


def test_update_user_success(mock_db, mocker) -> None:
    """Test the successful update of a user's information.

    This test validates that the `update_user` function correctly updates a user's
    information in the database and returns the updated user.
    """
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
    """Test updating a user that does not exist.

    This test ensures that the `update_user` function raises an HTTPException
    when the user is not found in the database.
    """
    updated_data = {"name": "New Name", "email": "new@example.com"}
    user_update = UserUpdate(**updated_data)
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Call the update_user function and assert the exception
    with pytest.raises(HTTPException) as exc_info:
        update_user(user_id=1, user=user_update, db=mock_db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


def test_delete_user_success(mock_db, mocker) -> None:
    """Test the successful deletion of a user.

    This test validates that the `delete_user` function correctly deletes a user
    from the database and returns a success message.
    """
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
    """Test deleting a user that does not exist.

    This test ensures that the `delete_user` function raises an HTTPException
    when the user is not found in the database.
    """
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Call the delete_user function and assert the exception
    with pytest.raises(HTTPException) as exc_info:
        delete_user(user_id=1, db=mock_db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"