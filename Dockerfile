# Use a base image with Python 3.10 pre-installed
FROM python:3.10-slim

# Set environment variables (Prevent Python from writing pyc files & set Python unbuffered mode)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry via pip
RUN pip install poetry

# Ensure poetry uses system python and does not create a venv
RUN poetry config virtualenvs.create false

# Copy the project files into the image
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# Copy the rest of the application
COPY . .

# Command to run the application
CMD ["python", "main.py"]
