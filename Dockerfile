# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Install the package
RUN pip install -e .

# Make port 80 available
EXPOSE 80

# Run the calculator application
CMD ["python", "-m", "calc"]

#dummy2