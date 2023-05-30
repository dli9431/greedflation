# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# setup virtual environment
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# If you have different requirements for this service, 
# then yes, you would need a separate requirements.txt file.
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
# Although note that Scrapy doesn't run as a server, so it might not need a port exposed
# EXPOSE 5000

# Run Scrapy or pytest when container launches (if environment variable is set)
CMD ["/bin/bash", "-c", "if [ \"$pytest\" = \"true\" ]; then pytest; else scrapy crawl initspider; fi"]
