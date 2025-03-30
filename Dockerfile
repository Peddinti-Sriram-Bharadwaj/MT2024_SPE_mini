# Use an official Ubuntu runtime as a parent image
FROM ubuntu:latest

# Set the working directory
WORKDIR /app

# Install required packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container
COPY . /app

# Set up a virtual environment and install dependencies
RUN python3 -m venv venv && \
    ./venv/bin/pip install --upgrade pip && \
    ./venv/bin/pip install -r requirements.txt && \
    ./venv/bin/pip install -e .[test]

# Define environment variable
ENV NAME Scientific_Calculator

# Make port 80 available to the world outside this container
EXPOSE 80

# Default command to run the calculator service
CMD ["./venv/bin/python", "-m", "scientific_calculator.app"]