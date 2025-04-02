"""Database connection and session management for the FastAPI application."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base  # Combined import for clarity
from dotenv import load_dotenv

# Load environment variables from a .env file into os.environ
load_dotenv()

# Retrieve the database URL from the environment variables.
# This URL should be formatted according to the requirements of your database.
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a SQLAlchemy engine instance.
# The engine establishes the core interface to the database.
# The 'connect_args' parameter here sets the timezone to UTC.
engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-c timezone=utc"}
)

# Create a configured "SessionLocal" class.
# This sessionmaker will generate new Session objects to interact with the database.
# 'autocommit=False' means changes need to be committed manually.
# 'autoflush=False' prevents automatic flushing of the session before queries.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our ORM models.
# All models should inherit from this Base class to be recognized by SQLAlchemy.
Base = declarative_base()


def get_db():
    """
    Dependency function for obtaining a new database session.

    This generator function creates a new session from SessionLocal,
    yields it for use (e.g., in FastAPI dependency injection), and ensures
    that the session is closed after use, even if an exception occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
