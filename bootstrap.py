#!/usr/bin/env python3
"""
Bootstrap script for the Ticket System project.
Sets up the development environment from scratch.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

class TicketBootstrapper:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.frontend_dir = self.root_dir / "frontend"
        self.backend_dir = self.root_dir / "myticket"
        self.venv_dir = self.root_dir / "venv"
        
    def check_prerequisites(self):
        """Check if required tools are installed"""
        print("🔍 Checking prerequisites...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 8):
            print(f"   ❌ Python 3.8+ required, found {python_version.major}.{python_version.minor}")
            return False
        print(f"   ✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✓ Node.js {result.stdout.strip()}")
            else:
                print("   ❌ Node.js not found")
                return False
        except FileNotFoundError:
            print("   ❌ Node.js not found")
            return False
            
        # Check npm
        try:
            result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✓ npm {result.stdout.strip()}")
            else:
                print("   ❌ npm not found")
                return False
        except FileNotFoundError:
            print("   ❌ npm not found")
            return False
            
        # Check git
        try:
            result = subprocess.run(["git", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✓ Git {result.stdout.split()[2]}")
            else:
                print("   ❌ Git not found")
                return False
        except FileNotFoundError:
            print("   ❌ Git not found")
            return False
            
        return True
        
    def create_virtual_environment(self):
        """Create Python virtual environment"""
        print("🐍 Creating virtual environment...")
        
        if self.venv_dir.exists():
            print("   ✓ Virtual environment already exists")
            return True
            
        try:
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_dir)], 
                         check=True, capture_output=True)
            print("   ✓ Virtual environment created")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to create virtual environment: {e}")
            return False
            
    def activate_virtual_environment(self):
        """Get the path to the virtual environment's Python and pip"""
        if os.name == "nt":  # Windows
            python_path = self.venv_dir / "Scripts" / "python.exe"
            pip_path = self.venv_dir / "Scripts" / "pip.exe"
        else:  # Unix/Linux/macOS
            python_path = self.venv_dir / "bin" / "python"
            pip_path = self.venv_dir / "bin" / "pip"
            
        return python_path, pip_path
        
    def install_backend_dependencies(self):
        """Install Python backend dependencies"""
        print("📦 Installing backend dependencies...")
        
        python_path, pip_path = self.activate_virtual_environment()
        
        # Upgrade pip
        try:
            subprocess.run([str(pip_path), "install", "--upgrade", "pip"], 
                         check=True, capture_output=True)
            print("   ✓ pip upgraded")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Failed to upgrade pip: {e}")
            
        # Install requirements
        requirements_file = self.root_dir / "requirements.txt"
        if requirements_file.exists():
            try:
                subprocess.run([str(pip_path), "install", "-r", str(requirements_file)], 
                             check=True, capture_output=True)
                print("   ✓ Backend dependencies installed")
                return True
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Failed to install backend dependencies: {e}")
                return False
        else:
            print("   ❌ requirements.txt not found")
            return False
            
    def install_frontend_dependencies(self):
        """Install Node.js frontend dependencies"""
        print("📦 Installing frontend dependencies...")
        
        if not self.frontend_dir.exists():
            print("   ❌ Frontend directory not found")
            return False
            
        os.chdir(self.frontend_dir)
        
        try:
            subprocess.run(["npm", "install"], check=True, capture_output=True)
            print("   ✓ Frontend dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install frontend dependencies: {e}")
            return False
            
    def setup_django(self):
        """Setup Django project"""
        print("⚙️  Setting up Django...")
        
        python_path, _ = self.activate_virtual_environment()
        manage_py = self.backend_dir / "manage.py"
        
        if not manage_py.exists():
            print("   ❌ manage.py not found")
            return False
            
        # Set Django settings
        env = os.environ.copy()
        env['DJANGO_SETTINGS_MODULE'] = 'myticket.settings'
        
        # Run migrations
        try:
            subprocess.run([str(python_path), str(manage_py), "makemigrations"], 
                         check=True, capture_output=True, cwd=self.backend_dir, env=env)
            print("   ✓ Django migrations created")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Failed to create migrations: {e}")
            
        try:
            subprocess.run([str(python_path), str(manage_py), "migrate"], 
                         check=True, capture_output=True, cwd=self.backend_dir, env=env)
            print("   ✓ Django migrations applied")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Failed to apply migrations: {e}")
            
        # Create superuser if database is empty
        try:
            result = subprocess.run([str(python_path), str(manage_py), "shell", "-c", 
                                   "from django.contrib.auth.models import User; print(User.objects.count())"], 
                                  capture_output=True, text=True, cwd=self.backend_dir, env=env)
            if result.returncode == 0 and result.stdout.strip() == "0":
                print("   ℹ️  Database is empty. You may want to create a superuser later.")
        except:
            pass
            
        return True
        
    def create_environment_file(self):
        """Create environment configuration file"""
        print("📝 Creating environment configuration...")
        
        env_file = self.root_dir / ".env"
        if env_file.exists():
            print("   ✓ .env file already exists")
            return True
            
        env_content = """# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
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
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Payment Settings (if using Stripe)
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
STRIPE_SECRET_KEY=your-stripe-secret-key

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
"""
        
        try:
            with open(env_file, 'w') as f:
                f.write(env_content)
            print("   ✓ .env file created")
            return True
        except Exception as e:
            print(f"   ❌ Failed to create .env file: {e}")
            return False
            
    def create_gitignore(self):
        """Create or update .gitignore file"""
        print("📝 Setting up .gitignore...")
        
        gitignore_file = self.root_dir / ".gitignore"
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# React
frontend/build/
frontend/.env.local
frontend/.env.development.local
frontend/.env.test.local
frontend/.env.production.local

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Temporary files
temp/
*.tmp
"""
        
        try:
            with open(gitignore_file, 'w') as f:
                f.write(gitignore_content)
            print("   ✓ .gitignore file created/updated")
            return True
        except Exception as e:
            print(f"   ❌ Failed to create .gitignore file: {e}")
            return False
            
    def create_scripts(self):
        """Create useful scripts for development"""
        print("📝 Creating development scripts...")
        
        # Create start script
        start_script = self.root_dir / "start_dev.py"
        start_content = """#!/usr/bin/env python3
\"\"\"
Development server startup script.
Starts both Django backend and React frontend.
\"\"\"

import subprocess
import sys
import time
from pathlib import Path

def start_backend():
    \"\"\"Start Django backend server\"\"\"
    root_dir = Path(__file__).parent
    backend_dir = root_dir / "myticket"
    venv_python = root_dir / "venv" / ("Scripts" / "python.exe" if sys.platform == "win32" else "bin" / "python")
    
    env = {"DJANGO_SETTINGS_MODULE": "myticket.settings"}
    
    print("🚀 Starting Django backend...")
    subprocess.Popen([str(venv_python), "manage.py", "runserver"], 
                     cwd=backend_dir, env=env)

def start_frontend():
    \"\"\"Start React frontend development server\"\"\"
    root_dir = Path(__file__).parent
    frontend_dir = root_dir / "frontend"
    
    print("🚀 Starting React frontend...")
    subprocess.Popen(["npm", "start"], cwd=frontend_dir)

if __name__ == "__main__":
    print("🎯 Starting development servers...")
    print("   Backend will be available at: http://localhost:8000")
    print("   Frontend will be available at: http://localhost:3000")
    print("   Press Ctrl+C to stop all servers")
    
    try:
        start_backend()
        time.sleep(2)  # Give backend time to start
        start_frontend()
        
        # Keep script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\n🛑 Stopping development servers...")
        sys.exit(0)
"""
        
        try:
            with open(start_script, 'w') as f:
                f.write(start_content)
            print("   ✓ Development startup script created")
        except Exception as e:
            print(f"   ⚠️  Failed to create startup script: {e}")
            
    def bootstrap(self):
        """Main bootstrap process"""
        print("🎯 Starting bootstrap process for Ticket System...")
        print("=" * 50)
        
        # Check prerequisites
        if not self.check_prerequisites():
            print("❌ Prerequisites check failed. Please install required tools.")
            return False
            
        # Create virtual environment
        if not self.create_virtual_environment():
            print("❌ Failed to create virtual environment.")
            return False
            
        # Install backend dependencies
        if not self.install_backend_dependencies():
            print("❌ Failed to install backend dependencies.")
            return False
            
        # Install frontend dependencies
        if not self.install_frontend_dependencies():
            print("❌ Failed to install frontend dependencies.")
            return False
            
        # Setup Django
        if not self.setup_django():
            print("❌ Failed to setup Django.")
            return False
            
        # Create configuration files
        self.create_environment_file()
        self.create_gitignore()
        self.create_scripts()
        
        print("=" * 50)
        print("🎉 Bootstrap completed successfully!")
        print("")
        print("Next steps:")
        print("1. Activate virtual environment:")
        if os.name == "nt":
            print("   venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        print("")
        print("2. Start development servers:")
        print("   python start_dev.py")
        print("")
        print("3. Or start servers separately:")
        print("   Backend:  cd myticket && python manage.py runserver")
        print("   Frontend: cd frontend && npm start")
        print("")
        print("4. Access your application:")
        print("   Backend:  http://localhost:8000")
        print("   Frontend: http://localhost:3000")
        print("   Admin:    http://localhost:8000/admin")
        
        return True

def main():
    bootstrapper = TicketBootstrapper()
    success = bootstrapper.bootstrap()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

