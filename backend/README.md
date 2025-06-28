# Mentor-Mentee Matching Backend

FastAPI-based backend for the mentor-mentee matching application.

## Setup

1. Install dependencies:
```bash
make install
```

2. Initialize the database:
```bash
make init-db
```

3. Run the application:
```bash
make run
```

4. Run tests:
```bash
make test
```

The backend will be available at:
- Main app: http://localhost:8080
- API endpoints: http://localhost:8080/api
- Swagger UI: http://localhost:8080/swagger-ui
- OpenAPI JSON: http://localhost:8080/openapi.json

## Features

- User authentication (signup/login) with JWT tokens
- User profile management with image upload
- Mentor listing and search functionality
- Matching request system
- Role-based access control (mentor/mentee)
- SQLite database with automatic initialization

## API Documentation

The API follows OpenAPI 3.0 specification and includes:
- Authentication endpoints
- User profile management
- Mentor search and filtering
- Matching request CRUD operations

All endpoints require Bearer token authentication except signup and login.

## Testing

The backend includes a comprehensive test suite covering:

- **Authentication**: Signup, login, JWT token validation
- **User Management**: Profile CRUD, image upload, role validation
- **Mentor System**: Search, filtering, sorting functionality
- **Matching Requests**: Full CRUD with status management
- **Database Models**: Relationships and constraints
- **Integration Tests**: Complete user workflows

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Test Structure

- `tests/test_auth.py` - Authentication endpoints
- `tests/test_users.py` - User profile management
- `tests/test_mentors.py` - Mentor listing and search
- `tests/test_matching.py` - Matching request system
- `tests/test_integration.py` - End-to-end workflows
- `tests/conftest.py` - Test fixtures and configuration

Tests use isolated SQLite databases and are automatically cleaned up.
