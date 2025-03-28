# Use an official Python runtime as a parent image
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user
RUN addgroup --system appgroup && adduser --system --group appuser

# Set the working directory
WORKDIR /app

# Copy the requirements files
COPY requirements.txt requirements-dev.txt ./

# Install dependencies based on the environment
ARG ENVIRONMENT=${ENVIRONMENT}
RUN if [ "$ENVIRONMENT" = "development" ]; then \
    pip install --no-cache-dir -r requirements-dev.txt; \
    else \
    pip install --no-cache-dir -r requirements.txt; \
    fi


# Copy the current directory contents into the container at /app
COPY . .

# Change ownership of the application directory
RUN chown -R appuser:appgroup /app

# Create the log directory and set permissions
RUN mkdir -p /var/log/app && \
    chown appuser:appgroup /var/log/app && \
    chmod 755 /var/log/app && \
    touch /var/log/app/fastapi.log && \
    chown appuser:appgroup /var/log/app/fastapi.log

# Switch to the non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Run the application. Do not use --reload in production as it is not recommended for performance and security reasons.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
