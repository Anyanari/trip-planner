# Trip Planner - Testing Guide

This document provides comprehensive information about the testing setup and how to run tests for the Trip Planner project.

## Overview

The Trip Planner project has comprehensive test coverage for both backend and frontend components:

- **Backend**: FastAPI + SQLAlchemy with pytest
- **Frontend**: React + TypeScript with Jest + React Testing Library
- **Coverage Target**: 85% for backend, 80% for frontend

## Test Structure

### Backend Tests

```
backend/
├── tests/
│   ├── conftest.py              # Test configuration and fixtures
│   ├── test_models/              # SQLAlchemy model tests
│   │   ├── test_user.py
│   │   ├── test_trip.py
│   │   ├── test_place.py
│   │   ├── test_expense.py
│   │   ├── test_suggestion.py
│   │   ├── test_route.py
│   │   └── test_trip_member.py
│   ├── test_routers/            # API endpoint tests
│   │   ├── test_users.py
│   │   ├── test_trips.py
│   │   ├── test_places.py
│   │   ├── test_expenses.py
│   │   ├── test_suggestions.py
│   │   └── test_routes.py
│   ├── test_services/           # Business logic tests
│   └── test_schemas/            # Pydantic schema tests
├── pytest.ini                  # pytest configuration
└── requirements.txt             # Includes test dependencies
```

### Frontend Tests

```
frontend/
├── src/
│   └── __tests__/
│       ├── components/           # React component tests
│       │   └── TripCard.test.tsx
│       ├── pages/               # Page component tests
│       ├── services/            # API service tests
│       │   └── api.test.ts
│       └── mocks/               # Mock server setup
│           └── server.ts
├── jest.config.js              # Jest configuration
├── setupTests.ts               # Test setup file
└── package.json               # Includes test dependencies
```

## Running Tests

### Quick Start

Use the provided test runner script:

```bash
# Make the script executable
chmod +x run-tests.sh

# Run all tests with coverage
./run-tests.sh
```

### Manual Test Execution

#### Backend Tests

```bash
cd backend

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_models/test_user.py

# Run tests with verbose output
pytest -v

# Run tests matching a pattern
pytest -k "test_user_creation"
```

#### Frontend Tests

```bash
cd frontend

# Install dependencies
npm install

# Run all tests
npm test

# Run tests with coverage
npm test -- --coverage --watchAll=false

# Run tests in watch mode
npm test

# Run specific test file
npm test -- TripCard.test.tsx

# Run tests matching a pattern
npm test -- --testNamePattern="renders"
```

## Test Coverage

### Backend Coverage Requirements

- **Target**: 85% minimum coverage
- **Tools**: pytest-cov
- **Report**: HTML report generated in `backend/htmlcov/`

### Frontend Coverage Requirements

- **Target**: 80% minimum coverage
- **Tools**: Jest coverage
- **Report**: HTML report generated in `frontend/coverage/lcov-report/`

### Coverage Reports

After running tests:

1. **Backend**: Open `backend/htmlcov/index.html` in your browser
2. **Frontend**: Open `frontend/coverage/lcov-report/index.html` in your browser

## Test Data and Fixtures

### Backend Fixtures

The `conftest.py` file provides common test fixtures:

- `db_session`: In-memory SQLite database session
- `client`: FastAPI test client
- `sample_user_data`: Sample user creation data
- `sample_trip_data`: Sample trip creation data

### Frontend Mocks

The `server.ts` file provides MSW mock handlers:

- Mock API responses for all endpoints
- Consistent test data across tests
- Network request interception

## Writing New Tests

### Backend Test Example

```python
def test_create_user_success(client, sample_user_data):
    """Test successful user creation."""
    response = client.post("/api/users/", json=sample_user_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == sample_user_data["email"]
    assert data["username"] == sample_user_data["username"]
```

### Frontend Test Example

```typescript
import { render, screen } from '@testing-library/react';
import { TripCard } from '../components/TripCard';

describe('TripCard', () => {
  it('renders trip information correctly', () => {
    render(<TripCard {...mockProps} />);
    
    expect(screen.getByText('Test Trip')).toBeInTheDocument();
  });
});
```

## CI/CD Integration

### GitHub Actions

The project includes automated testing via GitHub Actions:

- **Trigger**: On push/PR to main/develop branches
- **Jobs**:
  - Backend tests with PostgreSQL
  - Frontend tests with Node.js
  - Integration tests
  - Coverage reporting to Codecov

### Local Development

For local development with hot reload:

```bash
# Backend (with file watching)
pytest --cov=app -f

# Frontend (with watch mode)
npm test
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Ensure PostgreSQL is running
   - Check database connection string in conftest.py

2. **Import Errors in Tests**
   - Verify PYTHONPATH includes the app directory
   - Check virtual environment activation

3. **Frontend Test Errors**
   - Clear node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`
   - Check TypeScript configuration

4. **Coverage Failures**
   - Review uncovered lines in coverage report
   - Add tests for uncovered code paths

### Debug Mode

For debugging tests:

```bash
# Backend with debugging
pytest --pdb

# Frontend with debugging
npm test -- --no-cache --verbose
```

## Best Practices

1. **Test Naming**: Use descriptive test names that explain the scenario
2. **Test Isolation**: Each test should be independent
3. **Mock External Dependencies**: Use mocks for external services
4. **Coverage Quality**: Focus on meaningful tests, not just coverage numbers
5. **Regular Updates**: Keep tests updated with code changes

## Future Improvements

- [ ] Add E2E tests with Playwright
- [ ] Add performance testing
- [ ] Add visual regression testing
- [ ] Add contract testing between frontend and backend
- [ ] Add load testing for API endpoints

## Support

For questions about testing:

1. Check existing test files for examples
2. Review pytest and Jest documentation
3. Consult the project's issue tracker
4. Reach out to the development team
