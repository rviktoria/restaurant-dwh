# Use the official Python image as a base image
FROM python:latest

# Install cron package
RUN apt-get update && apt-get install -y cron

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script to the container
COPY . .

# Copy crontab schedule
COPY crontab /etc/cron.d/my-cron-job

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/my-cron-job

# Apply the cron job
RUN crontab /etc/cron.d/my-cron-job

# Create folder for cron logs
RUN mkdir -p /var/log/cron
RUN chmod -R 0755 /var/log/cron

# Copy the entrypoint script into the container
COPY entrypoint.sh /

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Set the entrypoint script as the entry point
ENTRYPOINT ["/entrypoint.sh"]