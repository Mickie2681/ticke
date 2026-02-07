# Multi-stage Dockerfile for Ticket System
# Stage 1: Build React frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY frontend/src ./src
COPY frontend/public ./public

# Build the app
RUN npm run build

# Stage 2: Python backend
FROM python:3.11-slim AS backend-builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Production image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=myticket.settings
ENV DJANGO_DEBUG=False

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd --create-home --shell /bin/bash app

# Set work directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend code
COPY myticket ./myticket

# Copy frontend build
COPY --from=frontend-builder /app/frontend/build ./myticket/staticfiles

# Copy static files
COPY myticket/static ./myticket/static

# Create necessary directories
RUN mkdir -p /app/media /app/staticfiles /app/logs

# Copy configuration files
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/gunicorn.conf.py /app/gunicorn.conf.py
COPY docker/entrypoint.sh /app/entrypoint.sh

# Set permissions
RUN chown -R app:app /app
RUN chmod +x /app/entrypoint.sh

# Switch to app user
USER app

# Expose ports
EXPOSE 8000 80

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Start the application
ENTRYPOINT ["/app/entrypoint.sh"]

