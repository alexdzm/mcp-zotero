# Generated by https://smithery.ai. See: https://smithery.ai/docs/config#dockerfile
# Use an official Python image as a parent image
FROM python:3.11-slim

# Set the working directory to /app inside the container
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt ./

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code to the container
COPY src/ /app/src/

# Make sure the Python script is executable
RUN chmod +x /app/src/server.py

# Set environment variables for the application
ENV ZOTERO_API_KEY=""
ENV ZOTERO_USER_ID=""

# Define the command to run the application
ENTRYPOINT ["python", "/app/src/server.py"]

# Optionally expose a port if the application serves on a specific port
# EXPOSE 3000 (uncomment and set the correct port if needed)
