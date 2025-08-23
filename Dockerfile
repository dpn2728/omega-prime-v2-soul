# Use an official lightweight Python image as a base.
FROM python:3.11-slim

# Set the working directory inside the container.
WORKDIR /app

# Set environment variables to ensure logs are sent correctly.
ENV PYTHONUNBUFFERED True

# Copy the list of required tools into the container.
COPY requirements.txt requirements.txt

# Install the tools.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire kingdom's code into the container.
COPY . .

# The final command to make the AI alive.
# Use Gunicorn, the professional server, to run our main application (main:app).
# It will automatically listen on the port provided by Cloud Run ($PORT).
# We set a long timeout (300 seconds) to allow for complex thinking.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 300 main:app
