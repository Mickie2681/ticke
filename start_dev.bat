@echo off
echo 🎯 Starting Ticket System Development Servers...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run bootstrap.py first to set up the project.
    echo.
    pause
    exit /b 1
)

REM Check if frontend dependencies are installed
if not exist "frontend\node_modules" (
    echo 📦 Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
    echo.
)

echo 🚀 Starting Django backend...
start "Django Backend" cmd /k "venv\Scripts\activate.bat && cd myticket && python manage.py runserver"

echo ⏳ Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo 🚀 Starting React frontend...
start "React Frontend" cmd /k "cd frontend && npm start"

echo.
echo 🎉 Development servers started!
echo.
echo 📍 Access your application:
echo    Frontend: http://localhost:3000
echo    Backend:  http://localhost:8000
echo    Admin:    http://localhost:8000/admin
echo.
echo 💡 Press any key to close this window...
pause >nul












