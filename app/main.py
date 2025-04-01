"""Main application file.

This file initializes the FastAPI application, sets up routes, middleware, and
lifespan events, and configures static file handling. It serves as the entry point
for the application and provides a scaffold for building FastAPI projects.
"""

from contextlib import asynccontextmanager
import asyncio
from typing import Generator, AsyncGenerator
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.core.database import engine, Base
from app.api.v1.routes import users
from app.app_logger import AppLogger

# Configure logging
# This sets up a custom logger for the application using the AppLogger class.
logger = AppLogger().get_logger()

# Create session factory
# This session factory is used to create database sessions for interacting with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Application startup and shutdown events
@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application startup and shutdown lifecycle events.

    This function handles tasks that need to be performed when the application starts
    and shuts down, such as database migrations and resource cleanup.

    Args:
        fastapi_app (FastAPI): The FastAPI application instance.

    Yields:
        None: Keeps the application running.
    """
    logger.info("Starting up... Running DB migrations")

    # Store DB engine and session factory in app state for global access
    fastapi_app.state.db_engine = engine
    fastapi_app.state.SessionLocal = SessionLocal

    # Database retry with exponential backoff
    retries = 5
    wait_time = 1  # Start with 1 second

    while retries > 0:
        try:
            # Run database migrations
            await asyncio.get_running_loop().run_in_executor(
                None, Base.metadata.create_all, fastapi_app.state.db_engine
            )
            logger.info("Database migration completed successfully.")
            break
        except OperationalError:
            retries -= 1
            logger.warning(
                "Database connection failed. Retrying in %.1f seconds... "
                "(%d retries left)",
                wait_time,
                retries,
            )
            await asyncio.sleep(wait_time)
            # Exponential backoff (caps at 10s)
            wait_time = min(wait_time * 2, 10)
    else:
        logger.error(
            "Failed to connect to the database after multiple attempts.")
        raise RuntimeError("Database connection failed")

    yield  # Keep application running

    # Cleanup tasks during shutdown
    logger.info("Shutting down... Closing database connections")
    await asyncio.get_running_loop().run_in_executor(None, app.state.db_engine.dispose)


# Initialize FastAPI app with optimized lifespan function
# The lifespan function handles startup and shutdown events.
app = FastAPI(title="FastAPI Scaffold", lifespan=lifespan)

# Include user-related routes
# This adds the user-related API endpoints under the "/users" prefix.
app.include_router(users.router, prefix="/users", tags=["Users"])

# Mount the static files directory
# This serves static files (e.g., favicon.ico) from the "app/static" directory.
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Serve the favicon.ico file.

    This endpoint serves the favicon for the application, which is typically displayed
    in the browser tab.
    """
    return FileResponse("app/static/favicon.ico")


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
    """Root endpoint.

    This is the default endpoint for the application. It provides a simple
    welcome message to indicate that the application is running.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to FastAPI Scaffold"}
