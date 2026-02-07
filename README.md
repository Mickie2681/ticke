# 🎫 Ticket System

A modern ticket management system built with Django (backend) and React (frontend), featuring event management, ticket sales, and payment processing.

## 🚀 Features

- **Event Management**: Create, edit, and manage events
- **Ticket Sales**: Sell tickets with various pricing tiers
- **Payment Processing**: Integrated payment gateway support
- **QR Code Generation**: Unique QR codes for each ticket
- **User Management**: User registration, authentication, and profiles
- **Admin Dashboard**: Comprehensive admin interface
- **API**: RESTful API for frontend and mobile apps
- **Real-time Updates**: WebSocket support for live updates

## 🏗️ Architecture

- **Backend**: Django 4.2 + Django REST Framework
- **Frontend**: React 18 + React Router
- **Database**: PostgreSQL (production) / SQLite (development)
- **Cache**: Redis
- **Task Queue**: Celery
- **Web Server**: Nginx + Gunicorn
- **Containerization**: Docker + Docker Compose

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Node.js 16+**
- **npm 8+**
- **Git**
- **Docker** (optional, for containerized deployment)

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ticket
   ```

2. **Run the bootstrap script**
   ```bash
   python bootstrap.py
   ```

3. **Start development servers**
   ```bash
   python start_dev.py
   ```

4. **Access your application**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - Admin: http://localhost:8000/admin

### Option 2: Manual Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install backend dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Setup Django**
   ```bash
   cd myticket
   python manage.py migrate
   python manage.py createsuperuser
   cd ..
   ```

5. **Start servers**
   ```bash
   # Terminal 1: Backend
   cd myticket && python manage.py runserver
   
   # Terminal 2: Frontend
   cd frontend && npm start
   ```

## 🛠️ Development

### Available Commands

The project includes a comprehensive Makefile for common tasks:

```bash
# View all available commands
make help

# Install dependencies
make install

# Build project
make build

# Start development servers
make dev

# Run tests
make test

# Clean build artifacts
make clean

# Create production distribution
make dist
```

### Python Scripts

- **`bootstrap.py`**: Complete project setup
- **`build.py`**: Build and package the application
- **`start_dev.py`**: Start both development servers

### Project Structure

```
ticket/
├── myticket/           # Django backend
│   ├── events/         # Event management app
│   ├── payments/       # Payment processing app
│   ├── myticket/       # Django project settings
│   └── manage.py       # Django management script
├── frontend/           # React frontend
│   ├── src/            # Source code
│   ├── public/         # Public assets
│   └── package.json    # Node.js dependencies
├── docker/             # Docker configuration
├── requirements.txt    # Python dependencies
├── Makefile           # Development tasks
├── docker-compose.yml # Docker services
└── README.md          # This file
```

## 🐳 Docker Deployment

### Development with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Production Deployment

```bash
# Build production image
docker build -t ticket-system .

# Run production container
docker run -p 80:80 -p 8000:8000 ticket-system
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Static Files
STATIC_URL=/static/
STATIC_ROOT=staticfiles/

# Media Files
MEDIA_URL=/media/
MEDIA_ROOT=media/

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Payment Settings
STRIPE_PUBLISHABLE_KEY=your-stripe-key
STRIPE_SECRET_KEY=your-stripe-secret

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Database Configuration

The system supports multiple database backends:

- **SQLite** (development): `sqlite:///db.sqlite3`
- **PostgreSQL** (production): `postgresql://user:pass@host:port/db`
- **MySQL**: `mysql://user:pass@host:port/db`

## 🧪 Testing

### Backend Tests

```bash
cd myticket
python manage.py test
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Run All Tests

```bash
make test
```

## 📦 Building for Production

### Create Distribution Package

```bash
make dist
```

This creates a `dist/` directory with:
- Built frontend assets
- Backend code (excluding development files)
- Configuration files
- Dependencies list

### Production Deployment Steps

1. **Build the application**
   ```bash
   make dist
   ```

2. **Deploy to server**
   ```bash
   scp -r dist/ user@server:/path/to/deployment
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

6. **Start with Gunicorn**
   ```bash
   gunicorn myticket.wsgi:application
   ```

## 🔒 Security

### Production Security Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS with SSL certificates
- [ ] Set up proper database permissions
- [ ] Configure CORS settings
- [ ] Set up rate limiting
- [ ] Enable security headers

### Security Headers

The application includes security headers:
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection
- Referrer-Policy

## 📊 Monitoring

### Health Checks

- **Application**: `/health/`
- **Database**: Django admin interface
- **Celery**: Flower monitoring at `/flower/`

### Logging

Logs are stored in:
- **Application**: `/app/logs/`
- **Nginx**: `/var/log/nginx/`
- **Gunicorn**: Application logs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Check the documentation
- Review the code examples

## 🔄 Updates

To update the project:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
make install

# Run migrations
make migrate

# Restart services
make restart
```

---

**Happy coding! 🎉**












