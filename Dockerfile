FROM python:3.11-slim
ENV PYTHONUNBUFFERED=True
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# This CMD is more robust. It uses an environment variable for PORT,
# but defaults to 8080 if it's not set (like in local docker run).
CMD exec gunicorn --bind :${PORT:-8080} --workers 1 --threads 8 --timeout 300 main:app
