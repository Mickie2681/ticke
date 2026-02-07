#!/usr/bin/env python3
"""
Build script for the Ticket System project.
Handles building both Django backend and React frontend.
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path

class TicketBuilder:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.frontend_dir = self.root_dir / "frontend"
        self.backend_dir = self.root_dir / "myticket"
        self.build_dir = self.root_dir / "dist"
        
    def clean(self):
        """Clean build artifacts"""
        print("🧹 Cleaning build artifacts...")
        
        # Clean frontend build
        frontend_build = self.frontend_dir / "build"
        if frontend_build.exists():
            shutil.rmtree(frontend_build)
            print("   ✓ Frontend build cleaned")
            
        # Clean dist directory
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
            print("   ✓ Dist directory cleaned")
            
        # Clean Python cache
        for pycache in self.root_dir.rglob("__pycache__"):
            shutil.rmtree(pycache)
        print("   ✓ Python cache cleaned")
        
    def install_frontend_deps(self):
        """Install frontend dependencies"""
        print("📦 Installing frontend dependencies...")
        
        if not (self.frontend_dir / "node_modules").exists():
            os.chdir(self.frontend_dir)
            result = subprocess.run(["npm", "install"], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"   ❌ Frontend dependency installation failed: {result.stderr}")
                return False
            print("   ✓ Frontend dependencies installed")
        else:
            print("   ✓ Frontend dependencies already installed")
        return True
        
    def build_frontend(self):
        """Build React frontend"""
        print("🔨 Building frontend...")
        
        os.chdir(self.frontend_dir)
        result = subprocess.run(["npm", "run", "build"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"   ❌ Frontend build failed: {result.stderr}")
            return False
        print("   ✓ Frontend built successfully")
        return True
        
    def install_backend_deps(self):
        """Install backend dependencies"""
        print("🐍 Installing backend dependencies...")
        
        # Check if virtual environment exists
        venv_path = self.root_dir / "venv"
        if not venv_path.exists():
            print("   ❌ Virtual environment not found. Please run bootstrap.py first.")
            return False
            
        # Install requirements
        pip_cmd = [str(venv_path / "Scripts" / "pip")] if os.name == "nt" else [str(venv_path / "bin" / "pip")]
        result = subprocess.run(pip_cmd + ["install", "-r", "requirements.txt"], 
                              capture_output=True, text=True, cwd=self.root_dir)
        if result.returncode != 0:
            print(f"   ❌ Backend dependency installation failed: {result.stderr}")
            return False
        print("   ✓ Backend dependencies installed")
        return True
        
    def collect_static(self):
        """Collect Django static files"""
        print("📁 Collecting static files...")
        
        manage_py = self.backend_dir / "manage.py"
        if not manage_py.exists():
            print("   ❌ manage.py not found")
            return False
            
        # Set Django settings
        env = os.environ.copy()
        env['DJANGO_SETTINGS_MODULE'] = 'myticket.settings'
        
        result = subprocess.run([sys.executable, str(manage_py), "collectstatic", "--noinput"],
                              capture_output=True, text=True, cwd=self.backend_dir, env=env)
        if result.returncode != 0:
            print(f"   ❌ Static file collection failed: {result.stderr}")
            return False
        print("   ✓ Static files collected")
        return True
        
    def run_tests(self):
        """Run tests for both frontend and backend"""
        print("🧪 Running tests...")
        
        # Backend tests
        print("   Testing backend...")
        manage_py = self.backend_dir / "manage.py"
        env = os.environ.copy()
        env['DJANGO_SETTINGS_MODULE'] = 'myticket.settings'
        
        result = subprocess.run([sys.executable, str(manage_py), "test"],
                              capture_output=True, text=True, cwd=self.backend_dir, env=env)
        if result.returncode != 0:
            print(f"   ❌ Backend tests failed: {result.stderr}")
            return False
        print("   ✓ Backend tests passed")
        
        # Frontend tests
        print("   Testing frontend...")
        os.chdir(self.frontend_dir)
        result = subprocess.run(["npm", "test", "--", "--watchAll=false"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"   ❌ Frontend tests failed: {result.stderr}")
            return False
        print("   ✓ Frontend tests passed")
        
        return True
        
    def create_distribution(self):
        """Create distribution package"""
        print("📦 Creating distribution package...")
        
        self.build_dir.mkdir(exist_ok=True)
        
        # Copy backend
        backend_dist = self.build_dir / "backend"
        if self.backend_dir.exists():
            shutil.copytree(self.backend_dir, backend_dist, ignore=shutil.ignore_patterns(
                '__pycache__', '*.pyc', 'venv', 'db.sqlite3', '.git'
            ))
            print("   ✓ Backend copied to distribution")
            
        # Copy frontend build
        frontend_build = self.frontend_dir / "build"
        if frontend_build.exists():
            frontend_dist = self.build_dir / "frontend"
            shutil.copytree(frontend_build, frontend_dist)
            print("   ✓ Frontend copied to distribution")
            
        # Copy requirements and other files
        shutil.copy2("requirements.txt", self.build_dir)
        shutil.copy2("README.md", self.build_dir)
        
        print(f"   ✓ Distribution created at {self.build_dir}")
        
    def build(self, clean=False, test=False, dist=False):
        """Main build process"""
        print("🚀 Starting build process...")
        
        if clean:
            self.clean()
            
        # Install dependencies
        if not self.install_frontend_deps():
            return False
        if not self.install_backend_deps():
            return False
            
        # Build frontend
        if not self.build_frontend():
            return False
            
        # Collect static files
        if not self.collect_static():
            return False
            
        # Run tests if requested
        if test:
            if not self.run_tests():
                return False
                
        # Create distribution if requested
        if dist:
            self.create_distribution()
            
        print("🎉 Build completed successfully!")
        return True

def main():
    parser = argparse.ArgumentParser(description="Build the Ticket System project")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts before building")
    parser.add_argument("--test", action="store_true", help="Run tests after building")
    parser.add_argument("--dist", action="store_true", help="Create distribution package")
    
    args = parser.parse_args()
    
    builder = TicketBuilder()
    success = builder.build(clean=args.clean, test=args.test, dist=args.dist)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
