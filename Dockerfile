FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy only the requirements file first to leverage Docker's caching mechanism
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set the volume for data persistence
VOLUME ["/data"]

# Copy files
COPY . /app

# Command to run the script
CMD ["python", "etl.py"]