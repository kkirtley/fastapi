"""Main application file."""
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.database import engine, Base, get_db  # Import get_db here
from app.core.config import settings
from app.api.v1.routes import users
from app.app_logger import logger

# Import the users router
from app.api.v1.routes.users import router as users_router

STATIC_DIR = Path("app/static")

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """ 
    Lifespan event for FastAPI application.
    This function initializes the database and handles startup and shutdown events.
    """
    logger.info("Application starting up...")

    # Initialize the database
    app.state.db_engine = engine
    max_retries = settings.DB_MAX_RETRIES
    base_wait_time = settings.DB_RETRY_BASE_DELAY
    max_wait_time = settings.DB_RETRY_MAX_DELAY

    for attempt in range(max_retries):
        try:
            await asyncio.get_running_loop().run_in_executor(
                None, Base.metadata.create_all, engine
            )
            logger.info("Database initialized successfully")
            break
        except OperationalError as e:
            wait_time = min(base_wait_time * (2 ** attempt), max_wait_time)
            logger.warning(
                "Database connection attempt %d failed: %s. Retrying in %.1fs...",
                attempt + 1, str(e), wait_time
            )
            if attempt == max_retries - 1:
                logger.error("Database initialization failed after %d attempts", max_retries)
                raise RuntimeError("Failed to initialize database") from e
            await asyncio.sleep(wait_time)

    yield

    logger.info("Application shutting down...")
    await asyncio.get_running_loop().run_in_executor(None, engine.dispose)
    logger.info("Database connections closed")

# Create FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.ENV != "production" else None,
    redoc_url=None
)

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"]
)

# Static files setup
if not STATIC_DIR.exists():
    logger.warning("Static directory %s does not exist", STATIC_DIR)
else:
    logger.info("Static directory %s found", STATIC_DIR)
    if not STATIC_DIR.is_dir():
        logger.error("%s is not a directory", STATIC_DIR)
    else:
        logger.info("Serving static files from %s", STATIC_DIR)
        if not STATIC_DIR.is_absolute():
            STATIC_DIR = STATIC_DIR.resolve()
            logger.info("Resolved static directory to %s", STATIC_DIR)
        if not STATIC_DIR.exists():
            logger.error("Static directory %s does not exist", STATIC_DIR)
        if not STATIC_DIR.is_dir():
            logger.error("%s is not a directory", STATIC_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR, html=True), name="static")

@app.get("/", response_model=dict)
async def root() -> dict:
    """ Root endpoint for the application."""
    return {"message": f"Welcome to {settings.PROJECT_NAME}!"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    """ Serve the favicon.ico file."""
    favicon_path = STATIC_DIR / "favicon.ico"
    if not favicon_path.exists():
        logger.warning("Favicon not found at %s", favicon_path)
    return FileResponse(favicon_path)

# Example route using get_db from database.py
@app.get("/health", response_model=dict)
async def health_check(db: Session = Depends(get_db)) -> dict:
    """ Health check endpoint."""
    db.execute("SELECT 1")  # Test DB connection
    return {"status": "healthy", "database": "connected"}


# Included Routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

# Add more routers as needed
