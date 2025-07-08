# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    gcc build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run the app with Gunicorn and Uvicorn workers
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000", "--workers", "2"]
