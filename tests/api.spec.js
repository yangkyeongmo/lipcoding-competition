import { test, expect } from '@playwright/test';

test.describe('API Integration Tests', () => {
  const API_BASE_URL = 'http://localhost:8080';

  test('should verify backend health endpoint', async ({ request }) => {
    const response = await request.get(`${API_BASE_URL}/health`);
    expect(response.ok()).toBeTruthy();
    
    const body = await response.json();
    expect(body).toHaveProperty('status', 'healthy');
  });

  test('should register a new user via API', async ({ request }) => {
    const timestamp = Date.now();
    const userData = {
      email: `apitest${timestamp}@example.com`,
      password: 'ApiTestPassword123!',
      name: 'API Test User',
      role: 'mentee',
      interests: 'API Testing'
    };

    const response = await request.post(`${API_BASE_URL}/api/signup`, {
      data: userData
    });

    expect(response.ok()).toBeTruthy();
    const body = await response.json();
    expect(body).toHaveProperty('message', 'User created successfully');
  });

  test('should login user via API and return JWT token', async ({ request }) => {
    // First register a user
    const timestamp = Date.now();
    const userData = {
      email: `loginapi${timestamp}@example.com`,
      password: 'LoginApiPassword123!',
      name: 'Login API Test User',
      role: 'mentee'
    };

    await request.post(`${API_BASE_URL}/api/signup`, {
      data: userData
    });

    // Then login
    const loginResponse = await request.post(`${API_BASE_URL}/api/login`, {
      data: {
        email: userData.email,
        password: userData.password
      }
    });

    expect(loginResponse.ok()).toBeTruthy();
    const loginBody = await loginResponse.json();
    expect(loginBody).toHaveProperty('token');
    expect(loginBody.token).toBeTruthy();
  });

  test('should fetch user profile with valid JWT token', async ({ request }) => {
    // Register and login to get token
    const timestamp = Date.now();
    const userData = {
      email: `profileapi${timestamp}@example.com`,
      password: 'ProfileApiPassword123!',
      name: 'Profile API Test User',
      role: 'mentor',
      expertise: 'API Testing'
    };

    await request.post(`${API_BASE_URL}/api/signup`, {
      data: userData
    });

    const loginResponse = await request.post(`${API_BASE_URL}/api/login`, {
      data: {
        email: userData.email,
        password: userData.password
      }
    });

    const { token } = await loginResponse.json();

    // Fetch profile
    const profileResponse = await request.get(`${API_BASE_URL}/api/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    expect(profileResponse.ok()).toBeTruthy();
    const profile = await profileResponse.json();
    expect(profile).toHaveProperty('email', userData.email);
    expect(profile).toHaveProperty('name', userData.name);
    expect(profile).toHaveProperty('role', userData.role);
  });

  test('should fetch mentors list', async ({ request }) => {
    // Create a mentee first to authenticate
    const timestamp = Date.now();
    const menteeData = {
      email: `listmentee${timestamp}@example.com`,
      password: 'MenteeListPassword123!',
      name: 'List Test Mentee',
      role: 'mentee',
      interests: 'React, Node.js'
    };

    await request.post(`${API_BASE_URL}/api/signup`, {
      data: menteeData
    });

    // Login as mentee
    const menteeLogin = await request.post(`${API_BASE_URL}/api/login`, {
      data: {
        email: menteeData.email,
        password: menteeData.password
      }
    });

    const { token: menteeToken } = await menteeLogin.json();

    // Create a mentor
    const mentorData = {
      email: `listmentor${timestamp}@example.com`,
      password: 'MentorListPassword123!',
      name: 'List Test Mentor',
      role: 'mentor',
      expertise: 'React, Node.js',
      bio: 'Experienced developer'
    };

    await request.post(`${API_BASE_URL}/api/signup`, {
      data: mentorData
    });

    // Fetch mentors as authenticated mentee
    const mentorsResponse = await request.get(`${API_BASE_URL}/api/mentors`, {
      headers: {
        'Authorization': `Bearer ${menteeToken}`
      }
    });
    expect(mentorsResponse.ok()).toBeTruthy();
    
    const mentors = await mentorsResponse.json();
    expect(Array.isArray(mentors)).toBeTruthy();
  });

  test('should create and fetch matching requests', async ({ request }) => {
    // Create mentor and mentee
    const timestamp = Date.now();
    
    const mentorData = {
      email: `requestmentor${timestamp}@example.com`,
      password: 'RequestMentorPassword123!',
      name: 'Request Test Mentor',
      role: 'mentor',
      expertise: 'JavaScript',
      bio: 'JS expert'
    };

    const menteeData = {
      email: `requestmentee${timestamp}@example.com`,
      password: 'RequestMenteePassword123!',
      name: 'Request Test Mentee',
      role: 'mentee',
      interests: 'JavaScript'
    };

    // Register both users
    const mentorSignup = await request.post(`${API_BASE_URL}/api/signup`, {
      data: mentorData
    });
    const menteeSignup = await request.post(`${API_BASE_URL}/api/signup`, {
      data: menteeData
    });

    // Login as mentee to get token
    const menteeLogin = await request.post(`${API_BASE_URL}/api/login`, {
      data: {
        email: menteeData.email,
        password: menteeData.password
      }
    });

    const { token: menteeToken } = await menteeLogin.json();

    // Login as mentor to get their ID
    const mentorLogin = await request.post(`${API_BASE_URL}/api/login`, {
      data: {
        email: mentorData.email,
        password: mentorData.password
      }
    });

    const { token: mentorToken } = await mentorLogin.json();

    // Get mentor profile to extract ID
    const mentorProfileResponse = await request.get(`${API_BASE_URL}/api/me`, {
      headers: {
        'Authorization': `Bearer ${mentorToken}`
      }
    });
    const mentorProfile = await mentorProfileResponse.json();

    // Create matching request
    const requestData = {
      mentor_id: mentorProfile.id,
      message: 'I would like to learn JavaScript from you.'
    };

    const createRequestResponse = await request.post(`${API_BASE_URL}/api/matching-requests`, {
      headers: {
        'Authorization': `Bearer ${menteeToken}`,
        'Content-Type': 'application/json'
      },
      data: requestData
    });

    expect(createRequestResponse.ok()).toBeTruthy();
    const createdRequest = await createRequestResponse.json();
    expect(createdRequest).toHaveProperty('mentor_id', requestData.mentor_id);
    expect(createdRequest).toHaveProperty('message', requestData.message);
    expect(createdRequest).toHaveProperty('status', 'pending');

    // Fetch matching requests
    const fetchRequestsResponse = await request.get(`${API_BASE_URL}/api/matching-requests`, {
      headers: {
        'Authorization': `Bearer ${menteeToken}`
      }
    });

    expect(fetchRequestsResponse.ok()).toBeTruthy();
    const requests = await fetchRequestsResponse.json();
    expect(Array.isArray(requests)).toBeTruthy();
    expect(requests.length).toBeGreaterThan(0);
    
    const foundRequest = requests.find(r => r.id === createdRequest.id);
    expect(foundRequest).toBeDefined();
  });

  test('should handle authentication errors', async ({ request }) => {
    // Try to access protected endpoint without token
    const response = await request.get(`${API_BASE_URL}/api/me`);
    expect(response.status()).toBe(403);
  });

  test('should validate input data', async ({ request }) => {
    // Try to register with invalid data
    const invalidData = {
      email: 'invalid-email',
      password: '123', // Too short
      name: '',
      role: 'invalid-role'
    };

    const response = await request.post(`${API_BASE_URL}/api/signup`, {
      data: invalidData
    });

    expect(response.status()).toBe(422); // Validation error
  });
});
