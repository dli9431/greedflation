# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add ARG for build
ARG build

# Copy the requirements file into the container
COPY requirements.txt .
COPY dev-requirements.txt .

# setup virtual environment
RUN python -m venv venv

# Install any needed packages specified in requirements.txt
RUN /bin/bash -c "source venv/bin/activate && if [ \"$build\" = \"production\" ]; then pip install --trusted-host pypi.python.org -r requirements.txt; else pip install --trusted-host pypi.python.org -r dev-requirements.txt; fi"

# Copy the current directory contents into the container at /app
COPY . /app

# Run Scrapy or pytest when container launches (if environment variable is set)
CMD ["/bin/bash", "-c", "source venv/bin/activate && if [ \"$build\" = \"production\" ]; then scrapy crawl initspider; else pytest; fi"]