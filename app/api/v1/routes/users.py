"""User management routes for creating and retrieving users."""
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.database import get_db

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.

    Args:
        user (UserCreate): The user data to create a new user.
        db (Session, optional): The database session dependency.

    Raises:
        HTTPException: If the email is already registered.

    Returns:
        User: The newly created user.
    """

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session, optional): The database session dependency.

    Returns:
        User: The user object if found.

    Raises:
        HTTPException: If the user is not found, raises a 404 HTTP exception.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
