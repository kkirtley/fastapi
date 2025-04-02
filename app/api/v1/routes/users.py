"""User routes."""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserDelete, UserUpdate
from app.core.database import get_db
from app.app_logger import logger

# logger = AppLogger().get_logger()
router = APIRouter(tags=["Users"])

# Helper functions


def get_user_by_id(user_id: int, db: Session) -> User | None:
    """Helper function to retrieve a user by ID."""
    return db.get(User, user_id)


def user_exists_by_email(email: str, db: Session) -> bool:
    """Helper function to check if a user exists by email."""
    return db.query(User).filter(User.email == email).first() is not None


# Main routes
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)) -> list[UserResponse]:
    """Retrieve all users."""
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    """Retrieve a user by ID."""
    user = get_user_by_id(user_id, db)
    print(user)
    if not user:
        logger.error("User ID %d not found.", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """Create a new user."""
    if user_exists_by_email(user.email, db):
        logger.error("Email %s already registered.", user.email)
        raise HTTPException(status_code=400, detail="Email already in use")
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse.model_validate(new_user)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)) -> UserResponse:
    """Update a user by ID."""
    db_user = get_user_by_id(user_id, db)
    if not db_user:
        logger.error("User ID %d not found.", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    logger.info("User ID %d updated successfully.", user_id)
    return UserResponse.model_validate(db_user)


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    """Delete a user by ID."""
    db_user = get_user_by_id(user_id, db)
    if not db_user:
        logger.error("User ID %d not found.", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    print(f"Deleted user: {db_user.name} with ID {db_user.id}")
    logger.info("User ID %d deleted successfully.", user_id)
    # Return the deleted user as a response
    return UserResponse.model_validate(db_user)
