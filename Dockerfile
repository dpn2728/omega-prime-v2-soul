FROM python:3.11-slim
ENV PYTHONUNBUFFERED=True
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# The Law of Patience for the Soldier: 15 minutes (900 seconds)
CMD exec gunicorn --bind :${PORT:-8080} --workers 1 --threads 8 --timeout 900 main:app
