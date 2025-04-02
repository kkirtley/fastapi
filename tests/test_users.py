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
from app.api.v1.routes.users import update_user, create_user, get_user, delete_user


# client = TestClient(app)  # Uncomment if you want to implement integration tests


@pytest.fixture
def mock_session(mocker):
    """Fixture to create a mock database session.

    This fixture uses the `mocker` pytest fixture to create an object that simulates
    a SQLAlchemy database session. It is used to test database interactions without
    requiring a real database connection.
    """
    return mocker.MagicMock(spec=Session)


@pytest.fixture
def mock_user():
    return User(id=1, name="Test User", email="test@example.com")


def test_create_user_success(mock_session, mocker) -> None:
    """Test the successful creation of a new user.

    This test validates that the `create_user` function correctly adds a new user
    to the database and returns the expected response.
    """
    # Prepare test data
    new_user_data = {"name": "New User", "email": "newuser@example.com"}
    user_create = UserCreate(**new_user_data)
    mocked_user = User(id=1, **new_user_data)

    # Mock the database methods
    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_session.add = mocker.MagicMock()
    mock_session.commit = mocker.MagicMock()
    mock_session.refresh = mocker.MagicMock(side_effect=lambda user: setattr(
        user, "id", 1))

    response = create_user(user=user_create, db=mock_session)
    validate_user = UserResponse.model_validate(mocked_user)

    assert response.model_dump() == validate_user.model_dump()

    # Assert the response
    assert isinstance(response, UserResponse)
    assert response.id == validate_user.id
    assert response.name == validate_user.name
    assert response.email == validate_user.email

    # Verify that the mocked methods were called
    args, _ = mock_session.add.call_args
    added_user = args[0]
    assert isinstance(added_user, User)
    assert added_user.name == new_user_data["name"]
    assert added_user.email == new_user_data["email"]


def test_create_user_duplicate_email(mock_session, mock_user) -> None:
    """Test creating a user with an email that already exists.

    This test ensures that the `create_user` function raises an HTTPException
    when attempting to create a user with a duplicate email.
    """
    user_create = UserCreate(name="New User", email="test@example.com")

    # Mock the query to simulate an existing user
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user

    # Call the create_user function and assert the exception
    with pytest.raises(HTTPException) as exc_info:
        create_user(user=user_create, db=mock_session)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Email already registered"


def test_get_user_success(mock_session, mock_user) -> None:
    """Test the successful retrieval of a user by ID.

    This test validates that the `get_user` function correctly retrieves a user
    from the database when the user exists.
    """

    mock_session.get.return_value = mock_user

    # Assert the response
    response = get_user(user_id=1, db=mock_session)
    assert isinstance(response, UserResponse)
    assert response.id == mock_user.id
    assert response.name == mock_user.name
    assert response.email == mock_user.email
    validate_user = UserResponse.model_validate(mock_user)
    assert response.model_dump() == validate_user.model_dump()


def test_get_user_not_found(mock_session) -> None:
    """Test the retrieval of a user by ID that does not exist.

    This test ensures that the `get_user` function raises an HTTPException
    when the user is not found in the database.
    """
    mock_session.get.return_value = None

    # Call the get_user function and assert the exception
    with pytest.raises(HTTPException) as exc_info:
        get_user(user_id=1, db=mock_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


def test_update_user_success(mock_session, mocker, mock_user) -> None:
    """Test the successful update of a user's information.

    This test validates that the `update_user` function correctly updates a user's
    information in the database and returns the updated user.
    """
    updated_data = {"name": "New Name",
                    "email": "new@example.com"}
    user_update = UserUpdate(**updated_data)
    mock_session.get.return_value = mock_user

    # Mock the commit and refresh methods
    mock_session.commit = mocker.MagicMock()
    mock_session.refresh = mocker.MagicMock()

    response = update_user(user_id=1, user=user_update, db=mock_session)

    # Assert the response
    assert isinstance(response, UserResponse)
    assert response.name == updated_data["name"]
    assert response.email == updated_data["email"]
    assert response.id == 1

    # Verify that the mocked methods were called
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(mock_user)


def test_update_user_not_found(mock_session) -> None:
    """Test updating a user that does not exist.

    This test ensures that the `update_user` function raises an HTTPException
    when the user is not found in the database.
    """
    updated_data = {"name": "New Name", "email": "new@example.com"}
    user_update = UserUpdate(**updated_data)
    mock_session.get.return_value = None  # Simulate that the user does not exist

    # Call the update_user function and assert the exception
    with pytest.raises(HTTPException) as exc_info:
        update_user(user_id=1, user=user_update, db=mock_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


def test_delete_user_success(mock_session, mocker, mock_user) -> None:
    """Test the successful deletion of a user.

    This test validates that the `delete_user` function correctly deletes a user
    from the database and returns a UserResponse object of the deleted user.
    """
    mock_session.get.return_value = mock_user

    # Mock the delete and commit methods
    mock_session.delete = mocker.MagicMock()
    mock_session.commit = mocker.MagicMock()

    # Call the delete_user function
    response = delete_user(user_id=1, db=mock_session)

    # Assert the response
    assert isinstance(response, UserResponse)
    assert response.id == 1
    assert response.name == mock_user.name
    assert response.email == mock_user.email
    assert response.model_dump() == UserResponse.model_validate(mock_user).model_dump()

    # Verify that the mocked methods were called
    mock_session.delete.assert_called_once_with(mock_user)
    mock_session.commit.assert_called_once()


def test_delete_user_not_found(mock_session) -> None:
    """Test deleting a user that does not exist.

    This test ensures that the `delete_user` function raises an HTTPException
    when the user is not found in the database.
    """
    mock_session.get.return_value = None  # Simulate that the user does not exist

    # Call the delete_user function and assert the exception
    with pytest.raises(HTTPException) as exc_info:
        delete_user(user_id=1, db=mock_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"
