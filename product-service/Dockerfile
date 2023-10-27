# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN pip install Flask pymongo

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 9996, which is the port that product microservice is running on
EXPOSE 9996


# Command to run the application when the container starts
CMD ["python3", "products.py"]
