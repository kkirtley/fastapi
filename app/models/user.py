""" User model definition."""
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    """
    User model for the application.

    Attributes:
        id (int): The primary key for the user.
        name (str): The name of the user.
        email (str): The unique email address of the user.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
