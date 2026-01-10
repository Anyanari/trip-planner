#!/bin/bash

# Trip Planner Test Runner
# This script runs all tests and checks coverage

set -e

echo "🧪 Running Trip Planner Test Suite"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "Starting test environment..."

# Start database for testing
print_status "Starting PostgreSQL for tests..."
docker-compose up -d postgres

# Wait for database to be ready
print_status "Waiting for database to be ready..."
sleep 10

# Backend tests
print_status "Running backend tests..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment and install dependencies
print_status "Installing backend dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Run backend tests with coverage
print_status "Running backend tests with coverage..."
pytest --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=85

BACKEND_EXIT_CODE=$?

cd ..

# Frontend tests
print_status "Running frontend tests..."
cd frontend

# Install dependencies
print_status "Installing frontend dependencies..."
npm ci

# Run frontend tests with coverage
print_status "Running frontend tests with coverage..."
npm test -- --coverage --watchAll=false

FRONTEND_EXIT_CODE=$?

cd ..

# Check results
print_status "Test Results Summary"
echo "======================="

if [ $BACKEND_EXIT_CODE -eq 0 ]; then
    print_status "✅ Backend tests passed with required coverage"
else
    print_error "❌ Backend tests failed or coverage below 85%"
fi

if [ $FRONTEND_EXIT_CODE -eq 0 ]; then
    print_status "✅ Frontend tests passed with required coverage"
else
    print_error "❌ Frontend tests failed or coverage below 80%"
fi

# Generate combined coverage report
print_status "Generating combined coverage report..."
echo "Backend coverage report: backend/htmlcov/index.html"
echo "Frontend coverage report: frontend/coverage/lcov-report/index.html"

# Cleanup
print_status "Cleaning up test environment..."
docker-compose down -v

# Exit with appropriate code
if [ $BACKEND_EXIT_CODE -eq 0 ] && [ $FRONTEND_EXIT_CODE -eq 0 ]; then
    print_status "🎉 All tests passed!"
    exit 0
else
    print_error "💥 Some tests failed!"
    exit 1
fi
