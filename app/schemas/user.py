""" User schemas. """
from typing import List
from pydantic import BaseModel, EmailStr


class BaseConfig(BaseModel):
    """ Base configuration for ORM models. """
    class Config:
        from_attributes = True

class UserCreate(BaseConfig):
    """ Schema for creating a new user. """
    name: str
    email: EmailStr

class UserResponse(BaseConfig):
    """ Schema for returning user data. """
    id: int
    name: str
    email: EmailStr

class UserDelete(BaseConfig):
    """ Schema for deleting a user. """
    id: int
    deleted: bool

class UserUpdate(UserResponse):
    """ Schema for updating a user. """
    updated: bool

class UserList(BaseConfig):
    """ Schema for listing users. """
    users: List[UserResponse]
