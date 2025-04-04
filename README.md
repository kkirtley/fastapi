# FastAPI Example Project

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This repository provides a minimal yet illustrative FastAPI application, including database integration and Docker support. It demonstrates how to:

- Set up a project with FastAPI
- Structure Python modules for clarity and maintainability
- Create endpoints with interactive API documentation
- Use Docker/Docker Compose to run both the FastAPI app and a PostgreSQL database
- Manage environment variables for local and containerized development

## Features

1. **High Performance**: Built on Starlette and Pydantic, making it suitable for production APIs.
2. **Interactive Documentation**: Automatically generated Swagger UI and ReDoc at runtime.
3. **Simple & Readable Codebase**: Minimal overhead, easy to understand and extend.
4. **Extensible**: Easily add new routes, data models, authentication, and more.
5. **Docker-Ready**: Includes a `Dockerfile` and `docker-compose.yml` for containerized development.
6. **Database Integration**: Sample database usage (e.g., PostgreSQL) via Docker Compose.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Local Development](#local-development)
  - [Docker Deployment](#docker-deployment)
  - [Docker Compose (App + Database)](#docker-compose-app--database)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Database](#database)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Project Structure

```
fastapi/
├── app/                     # Application code
│   ├── api/                 # API routes
│   ├── core/                # Core utilities (e.g., config, database)
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   └── main.py              # FastAPI app entry point
├── tests/                   # Test suite
├── .env.example             # Example environment variables
├── .gitignore               # Ignored files for Git
├── docker-compose.yml       # Compose file to run app + DB
├── Dockerfile               # Dockerfile for building the app image
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Prerequisites

- [Python 3.7+](https://www.python.org/downloads/) installed
- [pip](https://pip.pypa.io/en/stable/) for installing Python packages
- (Optional) [Docker](https://www.docker.com/) for containerized development
- (Optional) [Docker Compose](https://docs.docker.com/compose/) for multi-container setups
- (Recommended) [virtualenv](https://pypi.org/project/virtualenv/) or another environment tool to isolate dependencies

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/kkirtley/fastapi.git
   cd fastapi
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
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

Run the application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Base Endpoint**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Docker Deployment

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

1. **Configure Environment Variables**

   Copy `.env.example` to `.env` and set your environment variables (e.g., database credentials).

2. **Start Services**

   ```bash
   docker-compose up -d
   ```

   This will start the FastAPI app and a PostgreSQL database.

3. **Verify Containers**

   ```bash
   docker-compose logs -f
   ```

4. **Shut Down Services**

   ```bash
   docker-compose down --volumes --rmi all
   ```

## Environment Variables

Use a `.env` file to manage environment variables. Example:

```bash
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=fastapi_db
DB_HOST=db
DB_PORT=5432
```

## API Endpoints

- **GET /** – Returns a welcome message
- **Swagger UI** – `/docs`
- **ReDoc** – `/redoc`

## Database

This project uses PostgreSQL for database integration. Migrations can be managed using Alembic, and models are defined using SQLAlchemy.

## Testing

Run tests using `pytest`:

```bash
pytest
```

Ensure `pytest` and other testing dependencies are installed in `requirements.txt`.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Open a pull request

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to adapt this README as your project evolves!
