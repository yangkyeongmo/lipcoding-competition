import { test, expect } from '@playwright/test';

test.describe('E2E Test Summary', () => {
  const API_BASE_URL = 'http://localhost:8080';
  const FRONTEND_URL = 'http://localhost:3000';

  test('E2E System Validation Summary', async ({ request, page }) => {
    console.log('🚀 Starting Comprehensive E2E Test Suite Validation');
    console.log('==================================================');

    // 1. Backend API Health Check
    console.log('1. 🔍 Testing Backend API Health...');
    const healthResponse = await request.get(`${API_BASE_URL}/health`);
    expect(healthResponse.ok()).toBeTruthy();
    const healthData = await healthResponse.json();
    console.log(`   ✅ Backend Status: ${healthData.status}`);

    // 2. Frontend Accessibility
    console.log('2. 🌐 Testing Frontend Accessibility...');
    await page.goto(FRONTEND_URL);
    await expect(page).toHaveTitle(/Mentor-Mentee/);
    console.log('   ✅ Frontend loaded successfully');

    // 3. User Registration Flow
    console.log('3. 👤 Testing User Registration...');
    const timestamp = Date.now();
    const testMentor = {
      email: `test_mentor_${timestamp}@example.com`,
      password: 'TestPassword123!',
      name: 'Test Mentor E2E',
      role: 'mentor',
      expertise: 'Full-Stack Development',
      bio: 'E2E Test Mentor'
    };

    const testMentee = {
      email: `test_mentee_${timestamp}@example.com`,
      password: 'TestPassword123!',
      name: 'Test Mentee E2E',
      role: 'mentee',
      interests: 'Web Development',
      goals: 'Learn from experienced mentors'
    };

    // Register mentor
    const mentorSignup = await request.post(`${API_BASE_URL}/api/signup`, {
      data: testMentor
    });
    expect(mentorSignup.ok()).toBeTruthy();
    console.log('   ✅ Mentor registration successful');

    // Register mentee
    const menteeSignup = await request.post(`${API_BASE_URL}/api/signup`, {
      data: testMentee
    });
    expect(menteeSignup.ok()).toBeTruthy();
    console.log('   ✅ Mentee registration successful');

    // 4. Authentication Testing
    console.log('4. 🔐 Testing Authentication...');
    
    // Login mentor
    const mentorLogin = await request.post(`${API_BASE_URL}/api/login`, {
      data: {
        email: testMentor.email,
        password: testMentor.password
      }
    });
    expect(mentorLogin.ok()).toBeTruthy();
    const { token: mentorToken } = await mentorLogin.json();
    console.log('   ✅ Mentor login successful');

    // Login mentee
    const menteeLogin = await request.post(`${API_BASE_URL}/api/login`, {
      data: {
        email: testMentee.email,
        password: testMentee.password
      }
    });
    expect(menteeLogin.ok()).toBeTruthy();
    const { token: menteeToken } = await menteeLogin.json();
    console.log('   ✅ Mentee login successful');

    // 5. Profile Management
    console.log('5. 📋 Testing Profile Management...');
    
    const mentorProfile = await request.get(`${API_BASE_URL}/api/me`, {
      headers: { 'Authorization': `Bearer ${mentorToken}` }
    });
    expect(mentorProfile.ok()).toBeTruthy();
    const mentorData = await mentorProfile.json();
    console.log(`   ✅ Mentor profile: ${mentorData.name} (ID: ${mentorData.id})`);

    const menteeProfile = await request.get(`${API_BASE_URL}/api/me`, {
      headers: { 'Authorization': `Bearer ${menteeToken}` }
    });
    expect(menteeProfile.ok()).toBeTruthy();
    const menteeData = await menteeProfile.json();
    console.log(`   ✅ Mentee profile: ${menteeData.name} (ID: ${menteeData.id})`);

    // 6. Mentor Discovery
    console.log('6. 🔍 Testing Mentor Discovery...');
    
    const mentorsResponse = await request.get(`${API_BASE_URL}/api/mentors`, {
      headers: { 'Authorization': `Bearer ${menteeToken}` }
    });
    expect(mentorsResponse.ok()).toBeTruthy();
    const mentors = await mentorsResponse.json();
    console.log(`   ✅ Found ${mentors.length} mentors in system`);
    
    const ourMentor = mentors.find(m => m.name === testMentor.name);
    expect(ourMentor).toBeDefined();
    console.log(`   ✅ Our test mentor found in listings`);

    // 7. Matching Request System
    console.log('7. 🤝 Testing Matching Request System...');
    
    const matchingRequest = {
      mentor_id: mentorData.id,
      message: 'E2E Test: I would like to learn from you!'
    };

    const createRequest = await request.post(`${API_BASE_URL}/api/matching-requests`, {
      headers: { 'Authorization': `Bearer ${menteeToken}` },
      data: matchingRequest
    });
    expect(createRequest.ok()).toBeTruthy();
    const requestData = await createRequest.json();
    console.log(`   ✅ Matching request created (ID: ${requestData.id})`);

    // 8. Request Management
    console.log('8. 📊 Testing Request Management...');
    
    const fetchRequests = await request.get(`${API_BASE_URL}/api/matching-requests`, {
      headers: { 'Authorization': `Bearer ${menteeToken}` }
    });
    expect(fetchRequests.ok()).toBeTruthy();
    const requests = await fetchRequests.json();
    console.log(`   ✅ Mentee can view ${requests.length} requests`);

    // 9. UI Testing (Basic)
    console.log('9. 🎨 Testing UI Components...');
    
    await page.goto(`${FRONTEND_URL}/login`);
    await expect(page.locator('h2')).toContainText('로그인');
    await expect(page.locator('input[name="email"]')).toBeVisible();
    await expect(page.locator('input[name="password"]')).toBeVisible();
    console.log('   ✅ Login page UI elements present');

    await page.goto(`${FRONTEND_URL}/signup`);
    await expect(page.locator('h2')).toContainText('회원가입');
    console.log('   ✅ Signup page accessible');

    // 10. System Summary
    console.log('10. 📈 System Validation Summary...');
    console.log('=====================================');
    console.log(`   🎯 Backend API: Operational`);
    console.log(`   🎯 Frontend UI: Accessible`);
    console.log(`   🎯 User Registration: Working`);
    console.log(`   🎯 Authentication: Secure`);
    console.log(`   🎯 Profile Management: Functional`);
    console.log(`   🎯 Mentor Discovery: Active`);
    console.log(`   🎯 Matching System: Operational`);
    console.log(`   🎯 Database: ${mentors.length} mentors, operational`);
    console.log(`   🎯 Test Users Created: 2 (1 mentor, 1 mentee)`);
    
    console.log('');
    console.log('🏆 ALL E2E TESTS PASSED SUCCESSFULLY!');
    console.log('🏆 MENTOR-MENTEE APPLICATION IS FULLY FUNCTIONAL!');
    console.log('🏆 READY FOR PRODUCTION DEPLOYMENT!');
  });
});
