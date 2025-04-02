# FastAPI Example Project

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This repository provides a minimal yet illustrative FastAPI application, including a sample database integration. It demonstrates how to:

- Set up a project with FastAPI
- Structure Python modules for clarity
- Create endpoints and interactive API documentation
- Use Docker/Docker Compose to run both the FastAPI app and a Postgres database service
- Manage environment variables for local or containerized development

## Features

1. **High Performance**: Built on Starlette and Pydantic, making it suitable for production APIs.
2. **Interactive Documentation**: FastAPI automatically generates Swagger UI and ReDoc at runtime.
3. **Simple & Readable Codebase**: Minimal overhead, easy to understand and extend.
4. **Extensible**: Easily add new routes, data models, authentication, and more.
5. **Docker-Ready**: The project includes a Dockerfile and a `docker-compose.yml` file to run your app with a database.
6. **Database Integration**: Sample database usage (e.g., PostgreSQL) via Docker Compose.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Table of Contents](#table-of-contents)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Local Development](#local-development)
  - [Docker Deployment (Single Container)](#docker-deployment-single-container)
  - [Docker Compose (App + Database)](#docker-compose-app--database)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Database](#database)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Project Structure

A typical layout of this repository looks like this:

```
fastapi/
├── .env.example             # Example environment variables
├── .gitignore
├── docker-compose.yml       # Compose file to run app + DB
├── Dockerfile               # Dockerfile for building the app image
├── LICENSE
├── main.py                  # FastAPI app entry point
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

Depending on your version of the repository, there may be additional files or folders (e.g., `app`, `tests`, etc.). Below is a brief explanation of the core files:

- **main.py**: The primary FastAPI application with route definitions.
- **requirements.txt**: Lists Python dependencies needed for the app.
- **Dockerfile**: Defines how to build a Docker image for this project.
- **docker-compose.yml**: Defines services (FastAPI app and database) for multi-container Docker setups.
- **LICENSE**: MIT License details.
- **README.md**: Documentation to help you get started.

## Prerequisites

- [Python 3.7+](https://www.python.org/downloads/) installed
- [pip](https://pip.pypa.io/en/stable/) for installing Python packages
- (Optional) [Docker](https://www.docker.com/) if you plan to run the app in a container
- (Optional) [Docker Compose](https://docs.docker.com/compose/) if you plan to use the provided `docker-compose.yml`
- (Recommended) [virtualenv](https://pypi.org/project/virtualenv/) or another environment tool to keep dependencies isolated

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/kkirtley/fastapi.git
   cd fastapi
   ```

2. **Create a Virtual Environment** (recommended for local development)

   ```bash
   python3 -m venv venv
   # Activate the virtual environment (Linux/macOS):
   source venv/bin/activate

   # On Windows (cmd.exe):
   venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

You now have all required packages installed locally.

## Usage

### Local Development

You can run the application using Uvicorn (installed via `requirements.txt`):

```bash
uvicorn main:app --reload
```

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Base Endpoint**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Docker Deployment (Single Container)

If you only want to containerize the FastAPI app (without a separate database container):

1. **Build the Docker Image**

   ```bash
   docker build -t fastapi-example .
   ```

2. **Run the Docker Container**

   ```bash
   docker run -d --name fastapi-app -p 8000:8000 fastapi-example
   ```

3. **Access the Application**

   [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Docker Compose (App + Database)

If your project uses a database (e.g., PostgreSQL) and you want to run both the API and the database together:

1. **Configure Environment Variables**

   - Copy `.env.example` to `.env` (if provided) or set your own environment variables.
   - For example, you might specify database credentials and connection details in `.env`:
     ```bash
     DB_USER=postgres
     DB_PASSWORD=postgres
     DB_NAME=fastapi_db
     DB_HOST=db
     DB_PORT=5432
     ```

2. **Start Services with Docker Compose**

   ```bash
   docker-compose up -d
   ```

   This will spin up two containers:

   - `app` (FastAPI application) listening on port 8000
   - `db` (PostgreSQL database) listening on port 5432 inside the Docker network

3. **Verify Containers**

   - Check logs to ensure both containers are running correctly:
     ```bash
     docker-compose logs -f
     ```
   - The FastAPI app should be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).
   - 
4. *** Login to Container ***

   ```bash
   sudo docker exec -it [CONTAINER ID] /bin/sh
   ```

5. **Shut Down Services**

   ```bash
   docker-compose down
   ```

## Environment Variables

If your application requires environment variables, you can set them in a `.env` file. For example:

```bash
# Example .env
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=fastapi_db
DB_HOST=db
DB_PORT=5432
DEBUG=True
```

Then load them in your code (e.g., `main.py`) using [python-dotenv](https://pypi.org/project/python-dotenv/) or similar:

```python
from dotenv import load_dotenv
load_dotenv()

# Access them with:
# import os
# database_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
```

_(Note: This repo may not include `python-dotenv` by default, so you may need to install it.)_

## API Endpoints

In `main.py`, you might see a simple example endpoint:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World from FastAPI!"}
```

- **GET /** – returns a JSON message
- **Swagger UI** – `/docs`
- **ReDoc** – `/redoc`

For additional endpoints, open the interactive docs once the server is running.

## Database

If you are using a database (e.g., via Docker Compose), you may have additional code for:

- Database connections (e.g., SQLAlchemy)
- Migrations (e.g., Alembic)
- Models (Python classes representing your DB tables)

You can place these in separate modules or directly in `main.py` based on project complexity. The current repository may or may not include these details.

## Logging

Import the logger instance with the code below to inject into your files. 

from app.app_logger import logger

Use: logger.warn("These are not the droids you are looking for!")

## Testing

If you add tests or a testing framework (e.g., `pytest`), you can run them:

```bash
pytest
```

1. Ensure your dependencies (in `requirements.txt`) include `pytest`.
2. Store tests in a `tests/` directory or any pattern recognized by `pytest`.

## Contributing

Contributions, issues, and feature requests are welcome! If you’d like to contribute:

1. **Fork** this repository
2. **Create** a new branch for your feature or bug fix
3. **Commit** your changes with clear and concise messages
4. **Open** a pull request

If you plan to make any major changes, please open an issue first so we can discuss it.

## License

This project is licensed under the [MIT License](LICENSE). You’re free to use, modify, and distribute this code as permitted by the terms of that license.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) – A modern, high-performance web framework for building APIs with Python 3.7+.
- [Uvicorn](https://www.uvicorn.org/) – The lightning-fast ASGI server perfect for FastAPI.
- [Docker Compose](https://docs.docker.com/compose/) – Simplifies multi-container Docker applications.
- The broader open-source community for making libraries, tools, and knowledge freely available.

---

_Feel free to adapt and expand this README as your project grows. Happy coding with FastAPI!_
