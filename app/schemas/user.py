""" User schemas. """
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """ Schema for creating a new user."""
    name: str
    email: EmailStr

class UserResponse(UserCreate):
    """ Schema for user response."""
    id: int

    class ConfigDict:
        """ Configurations for the schema."""
        from_attributes = True
