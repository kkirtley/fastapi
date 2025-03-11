""" User schemas. """
from pydantic import BaseModel, EmailStr, ConfigDict

class BaseConfig(BaseModel):
    """ Base configuration for ORM models. """
    model_config = ConfigDict(from_attributes=True)

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
    