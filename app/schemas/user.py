"""User schemas."""

from typing import List
from pydantic import BaseModel, EmailStr


class BaseConfig(BaseModel):
    """Base configuration for ORM models."""

    model_config = {
        "from_attributes": True,
    }


class UserCreate(BaseConfig):
    """Schema for creating a new user."""

    name: str
    email: EmailStr


class UserResponse(BaseConfig):
    """Schema for returning user data."""

    id: int
    name: str
    email: EmailStr


class UserDelete(UserResponse):
    """Schema for deleting a user."""

    pass


class UserUpdate(UserCreate):
    """Schema for updating a user."""

    pass


class UserList(BaseConfig):
    """Schema for listing users."""

    users: List[UserResponse]
