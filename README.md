# FastAPI + PostgreSQL + Docker Scaffold

This project provides a well-structured FastAPI scaffold using PostgreSQL as the database and Docker for containerization.

## Features
- FastAPI for building APIs
- PostgreSQL as the database
- SQLAlchemy for ORM
- Alembic for migrations
- Docker for containerization
- Environment variables for configuration

## Setup

### Using Docker
```sh
docker-compose up --build
```

### Without Docker
```sh
uvicorn app.main:app --reload
```

## API Endpoints
- `POST /users/` - Create a user
- `GET /users/{id}` - Get user by ID

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.
