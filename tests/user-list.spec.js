import { test, expect } from '@playwright/test';

test.describe('User Management Tests', () => {
  const API_BASE_URL = 'http://localhost:8080';

  test('should show list of users created during testing', async ({ request }) => {
    console.log('=== Creating Test Users ===');
    
    // Create a few test users to demonstrate
    const users = [
      {
        email: `mentor1_${Date.now()}@example.com`,
        password: 'TestPassword123!',
        name: 'John Mentor',
        role: 'mentor',
        expertise: 'React, JavaScript, Node.js',
        bio: 'Senior full-stack developer with 5+ years experience'
      },
      {
        email: `mentor2_${Date.now()}@example.com`,
        password: 'TestPassword123!',
        name: 'Sarah Wilson',
        role: 'mentor',
        expertise: 'Python, Django, Machine Learning',
        bio: 'Data scientist and backend developer'
      },
      {
        email: `mentee1_${Date.now()}@example.com`,
        password: 'TestPassword123!',
        name: 'Mike Student',
        role: 'mentee',
        interests: 'Web Development, React',
        goals: 'Learn modern web development'
      },
      {
        email: `mentee2_${Date.now()}@example.com`,
        password: 'TestPassword123!',
        name: 'Emma Learner',
        role: 'mentee',
        interests: 'Data Science, Python',
        goals: 'Transition to data science career'
      }
    ];

    // Register all users
    const createdUsers = [];
    for (const userData of users) {
      console.log(`Creating user: ${userData.name} (${userData.role})`);
      
      const response = await request.post(`${API_BASE_URL}/api/signup`, {
        data: userData
      });
      
      expect(response.ok()).toBeTruthy();
      
      // Login to get user details
      const loginResponse = await request.post(`${API_BASE_URL}/api/login`, {
        data: {
          email: userData.email,
          password: userData.password
        }
      });
      
      const { token } = await loginResponse.json();
      
      // Get user profile
      const profileResponse = await request.get(`${API_BASE_URL}/api/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      const profile = await profileResponse.json();
      createdUsers.push({
        id: profile.id,
        name: profile.name,
        email: profile.email,
        role: profile.role,
        expertise: profile.expertise || 'N/A',
        interests: profile.interests || 'N/A'
      });
    }

    console.log('=== List of Created Users ===');
    createdUsers.forEach((user, index) => {
      console.log(`${index + 1}. ${user.name} (${user.role})`);
      console.log(`   Email: ${user.email}`);
      console.log(`   ID: ${user.id}`);
      if (user.role === 'mentor') {
        console.log(`   Expertise: ${user.expertise}`);
      } else {
        console.log(`   Interests: ${user.interests}`);
      }
      console.log('');
    });

    // Test mentor list functionality
    const mentee = createdUsers.find(u => u.role === 'mentee');
    const menteeLogin = await request.post(`${API_BASE_URL}/api/login`, {
      data: {
        email: users.find(u => u.role === 'mentee').email,
        password: 'TestPassword123!'
      }
    });
    
    const { token: menteeToken } = await menteeLogin.json();
    
    // Get mentors list
    const mentorsResponse = await request.get(`${API_BASE_URL}/api/mentors`, {
      headers: {
        'Authorization': `Bearer ${menteeToken}`
      }
    });
    
    expect(mentorsResponse.ok()).toBeTruthy();
    const mentors = await mentorsResponse.json();
    
    console.log('=== Mentors Available in System ===');
    mentors.forEach((mentor, index) => {
      console.log(`${index + 1}. ${mentor.name}`);
      console.log(`   Tech Stack: ${mentor.tech_stack || mentor.expertise || 'Not specified'}`);
      console.log(`   Bio: ${mentor.bio || 'No bio available'}`);
      console.log('');
    });

    expect(mentors.length).toBeGreaterThan(0);
    expect(createdUsers.length).toBe(4);
    
    console.log(`✅ Successfully created ${createdUsers.length} users`);
    console.log(`✅ Found ${mentors.length} mentors in the system`);
  });
});
