# Use an official Python runtime as a parent image
# This uses the slim version of Python 3.11 to reduce image size.
FROM python:3.11-slim AS base

# Set environment variables
# PYTHONDONTWRITEBYTECODE prevents Python from writing .pyc files to disk.
# PYTHONUNBUFFERED ensures that Python output is sent directly to the terminal without buffering.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user
# This improves security by running the application as a non-root user.
RUN addgroup --system appgroup && adduser --system --group appuser

# Set the working directory
# All subsequent commands will be run from the /app directory.
WORKDIR /app

# Copy the requirements files
# These files are used to install the necessary dependencies for the application.
COPY requirements.txt requirements-dev.txt ./

# Install dependencies based on the environment
# The ENVIRONMENT build argument determines whether to install development or production dependencies.
ARG ENVIRONMENT=${ENV}
RUN echo "BUILD ENVIRONMENT = $ENV"
RUN pip install --upgrade pip
RUN if [ "$ENVIRONMENT" = "development" ]; then \
    pip install --no-cache-dir -r requirements-dev.txt; \
    else \
    pip install --no-cache-dir -r requirements.txt; \
    fi

# Copy the current directory contents into the container at /app
# This includes the application source code and other necessary files.
COPY . .

# Change ownership of the application directory
# Ensures that the non-root user has ownership of the application files.
RUN chown -R appuser:appgroup /app

# Create the log directory and set permissions
# This ensures that the application can write logs to the specified directory.
RUN mkdir -p /var/log/app && \
    chown appuser:appgroup /var/log/app && \
    chmod 755 /var/log/app && \
    touch /var/log/app/fastapi.log && \
    chown appuser:appgroup /var/log/app/fastapi.log

# Switch to the non-root user
# All subsequent commands will be run as the non-root user for better security.
USER appuser

# Expose the port the app runs on
# This makes port 8000 available to the host machine.
EXPOSE 8000

# Run the application
# The CMD instruction specifies the command to run the FastAPI application using Uvicorn.
# Note: --reload is used for development purposes and should not be used in production.
# Conditionally use --reload if we're in development
CMD ["/bin/sh", "-c", "\
    if [ \"$ENVIRONMENT\" = \"development\" ]; then \
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload; \
    else \
    uvicorn app.main:app --host 0.0.0.0 --port 8000; \
    fi \
    "]