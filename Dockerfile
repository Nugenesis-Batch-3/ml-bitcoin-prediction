# Use the official Python base image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app


# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


    # Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /app/


# Install pipenv
RUN pip install pipenv


# Install dependencies
RUN pipenv install --deploy --ignore-pipfile


# Copy the application code
COPY . /app


# Expose the port that the app runs on
EXPOSE 5000


# Define environment variable
ENV FLASK_APP=app.py


# Command to run the application with Gunicorn
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
