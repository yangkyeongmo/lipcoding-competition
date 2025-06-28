# Mentor-Mentee Matching Application

A full-stack web application for matching mentors with mentees, built with FastAPI (Python) backend and React (JavaScript) frontend.

## Features

- **User Authentication**: JWT-based signup/login system
- **Profile Management**: User profiles with image upload support
- **Mentor Discovery**: Search and filter mentors by name and tech stack
- **Matching System**: Request-based mentor-mentee matching
- **Role-based Access**: Different interfaces for mentors and mentees
- **Real-time Updates**: Dynamic UI updates for matching requests

## Technology Stack

### Backend
- **Python 3.12** with FastAPI
- **SQLite** database with SQLAlchemy ORM
- **JWT** authentication with proper RFC 7519 claims
- **OpenAPI 3.0** documentation with Swagger UI
- **File upload** support for profile images

### Frontend
- **JavaScript** with React 18
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Axios** for API communication
- **Context API** for state management

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 22.x LTS
- Git

### Backend Setup
```bash
cd backend
make setup    # Install dependencies and initialize database
make run      # Start the server on http://localhost:8080
```

### Frontend Setup
```bash
cd frontend
make setup    # Install dependencies
make run      # Start the development server on http://localhost:3000
```

## Application URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8080/api
- **API Documentation**: http://localhost:8080/swagger-ui
- **OpenAPI Spec**: http://localhost:8080/openapi.json

## User Roles

### Mentee
- Browse and search mentors
- Send matching requests to mentors
- Manage their own requests (view, delete)
- Update profile with bio and image

### Mentor
- Receive matching requests from mentees
- Accept or reject requests (only one accepted request at a time)
- Update profile with bio, tech stack, and image
- View request history

## API Features

- **Authentication**: Signup, login with email/password
- **Profile Management**: CRUD operations with image upload
- **Mentor Listing**: Search, filter, and sort mentors
- **Matching Requests**: Full CRUD with status management
- **File Upload**: Profile image handling with validation

## Security

- JWT tokens with all RFC 7519 standard claims
- Password hashing with bcrypt
- Role-based access control
- File upload validation (type, size)
- CORS configuration for frontend integration

## Database Schema

- **Users**: Authentication, profile data, and role information
- **Matching Requests**: Request tracking with status management
- **Profile Images**: Stored as binary data in database

## Development

The application follows OpenAPI-first design principles with:
- Comprehensive API documentation
- Type-safe request/response handling
- Automated schema validation
- Error handling with proper HTTP status codes

For detailed setup and development instructions, see the README files in the `backend/` and `frontend/` directories.
