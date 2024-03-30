# Dockerfile to run the flask app

# Use the official image as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the content of the local src directory to the working directory
COPY . .

# Install with poetry
RUN python -m pip install --upgrade pip \
    && pip install poetry \
    && poetry install --no-dev --no-interaction

# Expose the logs
RUN ln -sf /dev/stdout /app/app.log

# Expose port 5000
EXPOSE 5000

# Run the flask app
CMD ["poetry", "run", "flask", "-A", "app/main.py", "run"]