#!/bin/bash

# Entrypoint script for Ticket System Docker container

set -e

echo "🚀 Starting Ticket System..."

# Function to handle shutdown gracefully
shutdown() {
    echo "🛑 Shutting down gracefully..."
    kill -TERM $NGINX_PID 2>/dev/null
    kill -TERM $GUNICORN_PID 2>/dev/null
    wait $NGINX_PID
    wait $GUNICORN_PID
    exit 0
}

# Set up signal handlers
trap shutdown SIGTERM SIGINT

# Create necessary directories
mkdir -p /app/logs /app/media /app/staticfiles

# Set proper permissions
chown -R app:app /app/logs /app/media /app/staticfiles

# Run database migrations
echo "🗄️ Running database migrations..."
cd /app/myticket
python manage.py migrate --noinput

# Collect static files if not already done
if [ ! -f /app/myticket/staticfiles/manifest.json ]; then
    echo "📁 Collecting static files..."
    python manage.py collectstatic --noinput
fi

# Start Gunicorn in background
echo "🐍 Starting Gunicorn..."
cd /app
gunicorn -c gunicorn.conf.py myticket.wsgi:application &
GUNICORN_PID=$!

# Wait a moment for Gunicorn to start
sleep 3

# Start Nginx in background
echo "🌐 Starting Nginx..."
nginx -g "daemon off;" &
NGINX_PID=$!

# Wait for both processes
wait $NGINX_PID $GUNICORN_PID

