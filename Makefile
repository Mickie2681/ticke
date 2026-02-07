# Makefile for Ticket System Project
# Provides common development tasks

.PHONY: help install bootstrap build clean test start stop dev frontend backend migrate superuser shell

# Default target
help:
	@echo "🎯 Ticket System - Available Commands:"
	@echo ""
	@echo "📦 Setup & Installation:"
	@echo "  install     - Install all dependencies (Python + Node.js)"
	@echo "  bootstrap   - Complete project setup from scratch"
	@echo ""
	@echo "🔨 Build & Development:"
	@echo "  build       - Build frontend and collect static files"
	@echo "  dev         - Start both development servers"
	@echo "  frontend    - Start React development server only"
	@echo "  backend     - Start Django development server only"
	@echo ""
	@echo "🧪 Testing & Quality:"
	@echo "  test        - Run all tests (frontend + backend)"
	@echo "  test-backend - Run Django tests only"
	@echo "  test-frontend - Run React tests only"
	@echo ""
	@echo "🗄️  Database:"
	@echo "  migrate     - Run Django migrations"
	@echo "  makemigrations - Create new Django migrations"
	@echo "  superuser   - Create Django superuser"
	@echo "  shell       - Open Django shell"
	@echo ""
	@echo "🧹 Maintenance:"
	@echo "  clean       - Clean build artifacts and cache"
	@echo "  stop        - Stop all development servers"
	@echo ""
	@echo "📦 Production:"
	@echo "  dist        - Create production distribution package"
	@echo "  docker      - Build and run with Docker"

# Check if we're on Windows
ifeq ($(OS),Windows_NT)
	PYTHON := venv\Scripts\python.exe
	PIP := venv\Scripts\pip.exe
	ACTIVATE := venv\Scripts\activate
	RM := rmdir /s /q
	MKDIR := mkdir
else
	PYTHON := venv/bin/python
	PIP := venv/bin/pip
	ACTIVATE := source venv/bin/activate
	RM := rm -rf
	MKDIR := mkdir -p
endif

# Install dependencies
install: install-backend install-frontend

install-backend:
	@echo "🐍 Installing Python dependencies..."
	$(PIP) install -r requirements.txt

install-frontend:
	@echo "📦 Installing Node.js dependencies..."
	cd frontend && npm install

# Bootstrap project from scratch
bootstrap:
	@echo "🚀 Bootstrapping project..."
	python bootstrap.py

# Build project
build: build-frontend collect-static

build-frontend:
	@echo "🔨 Building React frontend..."
	cd frontend && npm run build

collect-static:
	@echo "📁 Collecting Django static files..."
	cd myticket && $(PYTHON) manage.py collectstatic --noinput

# Development servers
dev:
	@echo "🎯 Starting development servers..."
	python start_dev.py

frontend:
	@echo "🚀 Starting React frontend..."
	cd frontend && npm start

backend:
	@echo "🐍 Starting Django backend..."
	cd myticket && $(PYTHON) manage.py runserver

# Testing
test: test-backend test-frontend

test-backend:
	@echo "🧪 Running Django tests..."
	cd myticket && $(PYTHON) manage.py test

test-frontend:
	@echo "🧪 Running React tests..."
	cd frontend && npm test -- --watchAll=false

# Database operations
migrate:
	@echo "🗄️ Running Django migrations..."
	cd myticket && $(PYTHON) manage.py migrate

makemigrations:
	@echo "🗄️ Creating Django migrations..."
	cd myticket && $(PYTHON) manage.py makemigrations

superuser:
	@echo "👤 Creating Django superuser..."
	cd myticket && $(PYTHON) manage.py createsuperuser

shell:
	@echo "🐍 Opening Django shell..."
	cd myticket && $(PYTHON) manage.py shell

# Clean up
clean:
	@echo "🧹 Cleaning build artifacts..."
	$(RM) frontend/build
	$(RM) dist
	$(RM) myticket/staticfiles
	$(RM) myticket/media
	find . -type d -name "__pycache__" -exec $(RM) {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleanup completed"

# Stop servers (Windows-specific)
stop:
	@echo "🛑 Stopping development servers..."
	taskkill /f /im node.exe 2>nul || echo "No Node.js processes found"
	taskkill /f /im python.exe 2>nul || echo "No Python processes found"

# Production distribution
dist: clean build
	@echo "📦 Creating production distribution..."
	$(MKDIR) dist
	cp -r myticket dist/backend
	cp -r frontend/build dist/frontend
	cp requirements.txt dist/
	cp README.md dist/ || echo "README.md not found"
	@echo "✅ Distribution package created in dist/"

# Docker commands
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t ticket-system .

docker-run:
	@echo "🐳 Running Docker container..."
	docker run -p 8000:8000 -p 3000:3000 ticket-system

docker: docker-build docker-run

# Quick development commands
run: dev
start: dev
serve: dev

# Alias for common commands
up: dev
down: stop
restart: stop dev

