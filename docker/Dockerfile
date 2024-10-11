# Use Python 3.11 slim base image
FROM python:3.11-slim as python-build

# Set the working directory
WORKDIR /workdir

# Install necessary build dependencies
RUN apt update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the working directory
COPY ./requirements.txt .

# Set up a virtual environment and install Python dependencies
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt

# Final stage: Create a lightweight runtime image
FROM python:3.11-slim

# Copy the virtual environment from the build stage
COPY --from=python-build /venv /venv

# Set the working directory for the application
WORKDIR /app

# Copy the application code to the working directory
COPY ./user_manager .

# Ensure that the virtual environment is used by default
ENV PATH="/venv/bin:$PATH"

# Specify the entry point for running the Python app
ENTRYPOINT ["python", "__main__.py"]
