# Use an official Python runtime as a parent image
FROM python:3.11.3-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the app code into the container
COPY . .

# Set the environment variable for the build
ENV FLASK_ENV=development

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define the command to run the app or tests when the container starts
CMD ["sh", "-c", "if [ \"$FLASK_ENV\" = \"test\" ]; then pytest; else python app.py; fi"]