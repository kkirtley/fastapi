"""User routes."""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserDelete, UserUpdate
from app.core.database import get_db
from app.app_logger import logger

router = APIRouter(tags=["Users"])

# Helper functions


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Helper function to retrieve a user by ID."""
    return db.get(User, user_id)


def user_exists_by_email(db: Session, email: str) -> bool:
    """Helper function to check if a user exists by email."""
    return db.query(User).filter(User.email == email).first() is not None


# Main routes
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)) -> list[User]:
    """Retrieve all users."""
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    """Retrieve a user by ID."""
    user = get_user_by_id(db, user_id)
    if not user:
        logger.error("User ID %d not found.", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    return user  # Directly return the ORM object mapped against the pydantic UserResponse model


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    """Create a new user."""
    if user_exists_by_email(db, user.email):
        logger.error("Email %s already registered.", user.email)
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)) -> User:
    """Update a user by ID."""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        logger.error("User ID %d not found.", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", response_model=UserDelete)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> UserDelete:
    """Delete a user by ID."""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        logger.error("User ID %d not found.", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return UserDelete(id=user_id, deleted=True)
