# FastAPI + PostgreSQL + Docker Scaffold

This project provides a well-structured FastAPI scaffold using PostgreSQL as the database and Docker for containerization.

## Features
- FastAPI for building APIs
- PostgreSQL as the database
- SQLAlchemy for ORM
- Alembic for migrations
- Docker for containerization
- Environment variables for configuration
- Health checks for services
- Non-root user for enhanced security

## Setup

### Using Docker

1. **Create a `.env` file**:
   Create a `.env` file in the root directory of your project with the following content:

   ```env
    POSTGRES_USER=myuser
    POSTGRES_PASSWORD=mypassword
    POSTGRES_DB=mydatabase
    POSTGRES_PORT=5432
    DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:${POSTGRES_PORT}/${POSTGRES_DB}
   ```

    Remove all docker containers, networks, volumes and images in development
    ```
    docker-compose down --rmi all -v
    ```
2. **Stop and remove containers, networks, volumes, and images**:
   Use the following command to stop and remove all containers, networks, volumes, and images:

   ```sh
   docker-compose down --rmi all
   ```

2. **Build and run the containers**:
   Use the following command to build and run the containers:

   ```sh
   docker-compose up --build
   ```

## API Endpoints
- `POST /users/` - Create a user
- `GET /users/{id}` - Get user by ID
- `PUT /users/{id}` - Update user by ID
- `DELETE /users/{id}` - Delete user by ID
- `GET /users/` - List all users

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

## Health Checks
- The `db` service has a health check to ensure the PostgreSQL database is running.
- The `api` service has a health check to ensure the FastAPI application is running.

## Security
- The application runs as a non-root user for enhanced security.