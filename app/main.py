"""Main application file"""

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
logger = AppLogger().get_logger()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Application startup and shutdown events
@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application startup and shutdown lifecycle events."""
    logger.info("Starting up... Running DB migrations")

    # Store DB engine and session factory in app state
    fastapi_app.state.db_engine = engine
    fastapi_app.state.SessionLocal = SessionLocal

    # Database retry with exponential backoff
    retries = 5
    wait_time = 1  # Start with 1 second

    while retries > 0:
        try:
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
# Mount the static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Serve the favicon.ico file."""
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
    """Root endpoint."""
    return {"message": "Welcome to FastAPI Scaffold"}
