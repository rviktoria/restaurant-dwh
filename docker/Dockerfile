# Use the official Python image as a base image
FROM python:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script to the container
COPY . .

# Run the Python script when the container starts
CMD ["python", "main.py"]
