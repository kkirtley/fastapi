"""Main application file"""

import logging
from contextlib import asynccontextmanager
import asyncio
from typing import Generator, AsyncGenerator
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, Depends
from app.core.database import engine, Base
from app.api.v1.routes import users
from app.models.user import User
from app.schemas.user import UserList

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Application startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application startup and shutdown lifecycle events."""
    logger.info("Starting up... Running DB migrations")

    # Store DB engine and session factory in app state
    app.state.db_engine = engine
    app.state.SessionLocal = SessionLocal

    # Database retry with exponential backoff
    retries = 5
    wait_time = 1  # Start with 1 second

    while retries > 0:
        try:
            await asyncio.get_running_loop().run_in_executor(
                None, Base.metadata.create_all, app.state.db_engine
            )
            logger.info("Database migration completed successfully.")
            break
        except OperationalError:
            retries -= 1
            logger.warning("Database connection failed. Retrying in %.1f seconds... "
            "(%d retries left)", wait_time, retries)
            await asyncio.sleep(wait_time)
            wait_time = min(wait_time * 2, 10)  # Exponential backoff (caps at 10s)
    else:
        logger.error("Failed to connect to the database after multiple attempts.")
        raise RuntimeError("Database connection failed")

    yield  # Keep application running

    logger.info("Shutting down... Closing database connections")
    await asyncio.get_running_loop().run_in_executor(None, app.state.db_engine.dispose)


# Initialize FastAPI app with optimized lifespan function
app = FastAPI(title="FastAPI Scaffold", lifespan=lifespan)
app.include_router(users.router, prefix="/users", tags=[])

# Dependency to get database session
def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a SQLAlchemy database session.

    This function is a generator that yields a database session object.
    It ensures that the session is properly closed after use.

    Yields:
        db (Session): A SQLAlchemy database session.
    """
    db = app.state.SessionLocal()  # Get session from app state
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {"message": "Welcome to FastAPI Scaffold"}
