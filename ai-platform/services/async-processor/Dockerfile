FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose ports for API and Flower monitoring
EXPOSE 8000 5555

# Set the command to run the API server and Celery worker
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & celery -A worker.celery_app worker --loglevel=info & celery -A worker.celery_app flower --port=5555"]
