# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the local app files to the container's working directory
COPY . /app

# Install the dependencies
RUN pip install --no-cache-dir flask mysql-connector-python

# Expose port 5000 to allow access to the Flask app
EXPOSE 5000

# Set the command to run the Flask app
CMD ["python", "app.py"]