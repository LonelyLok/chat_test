# Use Python 3.10-slim as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy all files from the current folder to the container, excluding __pycache__
COPY . .
RUN rm -rf **/__pycache__

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Run the Python script
CMD ["python3", "app.py"]