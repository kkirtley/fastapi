""" User routes. """
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserDelete, UserUpdate
from app.core.database import get_db

router = APIRouter(tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """ Create a new user."""
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserResponse.model_validate(new_user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    """ Retrieve a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)

@router.put("/{user_id}", response_model=UserUpdate)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)) -> UserUpdate:
    """ Update a user by ID."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return UserUpdate.model_validate(db_user)

@router.delete("/{user_id}", response_model=UserDelete)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> UserDelete:
    """ Delete a user by ID."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return UserDelete(id=user_id, deleted=True)