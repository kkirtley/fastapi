""" Testing LIfespan of FastAPI application """
from unittest.mock import patch
from sqlalchemy.exc import OperationalError
import pytest
from fastapi.testclient import TestClient


from app.main import app


def test_lifespan_success():
    """
    Test that the application starts and shuts down correctly using lifespan.
    """
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to FastAPI Scaffold!"}
        assert hasattr(app.state, "SessionLocal")
        assert hasattr(app.state, "db_engine")


def raise_operational_error(*args, **kwargs):
    """ Simulate an operational error when creating the database tables. """
    raise OperationalError("Simulated DB error", None, None)


def test_lifespan_startup_failure():
    """
    Test that the application raises RuntimeError after failing to connect to DB.
    """
    with patch("app.main.Base.metadata.create_all", side_effect=raise_operational_error):
        with pytest.raises(RuntimeError, match="Database connection failed"):
            with TestClient(app):
                pass  # Triggers lifespan


def test_favicon_route():
    """
    Test the favicon route returns 200 and correct content type.
    """
    with TestClient(app) as client:
        response = client.get("/favicon.ico")
        assert response.status_code == 200
        assert response.headers["content-type"] in {"image/x-icon", "image/vnd.microsoft.icon"}
