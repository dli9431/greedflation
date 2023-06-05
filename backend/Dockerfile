# Use an official Python runtime as a parent image
FROM python:3.11.3-slim-buster

# Set the working directory to /app
WORKDIR /app

# Add ARG for build
ARG build

# Copy the requirements file into the container
COPY requirements.txt .
COPY dev-requirements.txt .

# setup virtual environment and install dependencies
RUN python -m venv /venv
RUN /venv/bin/pip install --upgrade pip
RUN if [ "$build" = "production" ]; then \
        /venv/bin/pip install --trusted-host pypi.python.org -r requirements.txt; \
    else \
        /venv/bin/pip install --trusted-host pypi.python.org -r dev-requirements.txt; \
    fi

# Copy the current directory contents into the container at /app
COPY . /app

# Set the environment variable for the build
ENV FLASK_ENV=${build}

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define the command to run the app or tests when the container starts
CMD ["/bin/bash", "-c", "source /venv/bin/activate && if [ \"$FLASK_ENV\" = \"test\" ]; then pytest; else python app.py; fi"]