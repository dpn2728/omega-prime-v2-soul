# Base Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Ensure logs are printed immediately
ENV PYTHONUNBUFFERED=1

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# CMD for Cloud Run (Gunicorn listens on $PORT at runtime)
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "--workers", "1", "--threads", "8", "--timeout", "300", "main:app"]
