FROM python:3.11-slim as python-build
# Set the working directory
WORKDIR /workdir

# Install specific versions of Python and Nginx and other dependencies
RUN apt update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt  .


RUN python3 -m venv /venv && \
    . /venv/bin/activate && \
    pip install -r requirements.txt \

COPY --from=python-build /venv /venv

# Copy your Python backend code
COPY ./user_manager .

ENTRYPOINT ["python", "__main__.py"]
