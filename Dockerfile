FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a startup script
RUN echo '#!/bin/sh\necho "PORT is: $PORT"\nuvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8080

# Run the application
CMD ["/app/start.sh"]
