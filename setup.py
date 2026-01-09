#!/usr/bin/env python3
"""
Trip Planner - Setup and Test Script
This script helps set up the development environment and runs tests.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a command and return the result."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def check_prerequisites():
    """Check if required tools are installed."""
    print("Checking prerequisites...")
    
    # Check Docker
    try:
        run_command("docker --version")
        print("✓ Docker is installed")
    except:
        print("✗ Docker is not installed. Please install Docker first.")
        return False
    
    # Check Docker Compose
    try:
        run_command("docker-compose --version")
        print("✓ Docker Compose is installed")
    except:
        print("✗ Docker Compose is not installed. Please install Docker Compose first.")
        return False
    
    # Check Node.js
    try:
        run_command("node --version")
        print("✓ Node.js is installed")
    except:
        print("✗ Node.js is not installed. Please install Node.js first.")
        return False
    
    # Check Python
    try:
        run_command("python --version")
        print("✓ Python is installed")
    except:
        print("✗ Python is not installed. Please install Python first.")
        return False
    
    return True

def setup_backend():
    """Set up the backend environment."""
    print("\nSetting up backend...")
    
    backend_dir = Path("backend")
    
    # Create virtual environment
    if not (backend_dir / "venv").exists():
        print("Creating virtual environment...")
        run_command("python -m venv venv", cwd=backend_dir)
    
    # Install dependencies
    print("Installing Python dependencies...")
    if sys.platform == "win32":
        pip_path = backend_dir / "venv" / "Scripts" / "pip"
    else:
        pip_path = backend_dir / "venv" / "bin" / "pip"
    
    run_command(f"{pip_path} install -r requirements.txt", cwd=backend_dir)
    
    # Create .env file if it doesn't exist
    env_file = backend_dir / ".env"
    if not env_file.exists():
        print("Creating .env file...")
        env_content = """# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tripplanner

# Security
SECRET_KEY=your-super-secret-jwt-key-change-in-production

# Application Settings
DEBUG=true
APP_NAME=Trip Planner API
"""
        env_file.write_text(env_content)
    
    print("✓ Backend setup complete")

def setup_frontend():
    """Set up the frontend environment."""
    print("\nSetting up frontend...")
    
    frontend_dir = Path("frontend")
    
    # Install dependencies
    print("Installing Node.js dependencies...")
    run_command("npm install", cwd=frontend_dir)
    
    print("✓ Frontend setup complete")

def run_tests():
    """Run all tests."""
    print("\nRunning tests...")
    
    # Backend tests
    print("Running backend tests...")
    backend_dir = Path("backend")
    if sys.platform == "win32":
        python_path = backend_dir / "venv" / "Scripts" / "python"
    else:
        python_path = backend_dir / "venv" / "bin" / "python"
    
    run_command(f"{python_path} -m pytest tests/ -v", cwd=backend_dir, check=False)
    
    # Frontend tests
    print("Running frontend tests...")
    run_command("npm test -- --coverage --watchAll=false", cwd=Path("frontend"), check=False)

def start_services():
    """Start all services using Docker Compose."""
    print("\nStarting services...")
    run_command("docker-compose up --build -d")
    
    print("\nServices are starting up...")
    print("Frontend: http://localhost:3000")
    print("Backend API: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Database Admin: http://localhost:5050")
    
    print("\nTo stop services, run: docker-compose down")

def main():
    """Main function."""
    print("Trip Planner - Setup Script")
    print("=" * 40)
    
    if not check_prerequisites():
        sys.exit(1)
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Setup backend
    setup_backend()
    
    # Setup frontend
    setup_frontend()
    
    # Run tests
    run_tests()
    
    print("\nSetup complete!")
    print("To start the application, run:")
    print("python setup.py start")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "start":
        start_services()
    else:
        main()
