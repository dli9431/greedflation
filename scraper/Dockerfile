# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add ARG for build
ARG build

# Copy the requirements file into the container
COPY requirements.txt .
COPY dev-requirements.txt .

# setup virtual environment and install dependencies
RUN python -m venv /venv && \
    if [ "$build" = "prod" ]; then \
        /venv/bin/pip install --trusted-host pypi.python.org -r requirements.txt; \
    else \
        /venv/bin/pip install --trusted-host pypi.python.org -r dev-requirements.txt; \
    fi

# Copy the current directory contents into the container at /app
COPY . /app

# Run Scrapy or pytest when container launches (if environment variable is set)
CMD if [ "$BUILD_ENV" = "test" ]; then \
        /bin/bash -c "source /venv/bin/activate && python -m pytest"; \
    else \
        /bin/bash -c "source /venv/bin/activate && python -m scrapy crawl superstore_spider"; \
    fi
