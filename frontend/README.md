# Mentor-Mentee Matching Frontend

React-based frontend for the mentor-mentee matching application.

## Setup

1. Install dependencies:
```bash
make install
```

2. Run the development server:
```bash
make run
```

The frontend will be available at http://localhost:3000

## Features

- User authentication (login/signup)
- Profile management with image upload
- Mentor search and filtering (for mentees)
- Matching request management
- Responsive design with Tailwind CSS
- Role-based UI (mentor/mentee views)

## Pages

- `/login` - User login
- `/signup` - User registration
- `/profile` - User profile management
- `/mentors` - Mentor listing and search (mentees only)
- `/matching-requests` - Matching request management

## Technology Stack

- React 18
- React Router DOM for routing
- Axios for API communication
- Tailwind CSS for styling
- Context API for state management

## API Integration

The frontend communicates with the backend API at http://localhost:8080/api and automatically handles:
- JWT token management
- Authentication state
- API error handling
- File uploads
