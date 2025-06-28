import { test, expect } from '@playwright/test';

test.describe('Full User Journey Integration Tests', () => {
  test('complete mentor-mentee matching workflow', async ({ page, context }) => {
    const timestamp = Date.now();
    
    // Step 1: Register a mentor
    const mentorEmail = `journey_mentor_${timestamp}@example.com`;
    const mentorPassword = 'MentorJourney123!';
    
    await page.goto('/signup');
    await page.fill('input[name="email"]', mentorEmail);
    await page.fill('input[name="password"]', mentorPassword);
    await page.fill('input[name="confirmPassword"]', mentorPassword);
    await page.fill('input[name="name"]', 'Journey Test Mentor');
    await page.selectOption('select[name="role"]', 'mentor');
    await page.fill('input[name="expertise"]', 'Full-Stack Development, React, Node.js');
    await page.fill('textarea[name="bio"]', 'Senior developer with 8+ years of experience in web development.');
    await page.click('button[type="submit"]');
    
    // Verify mentor registration and dashboard
    await expect(page).toHaveURL(/\/(login|dashboard)/);
    
    if (page.url().includes('/login')) {
      await page.fill('input[name="email"]', mentorEmail);
      await page.fill('input[name="password"]', mentorPassword);
      await page.click('button[type="submit"]');
    }
    
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Mentor Dashboard');
    
    // Step 2: Create a mentee in a new browser context
    const menteeContext = await context.newPage();
    const menteeEmail = `journey_mentee_${timestamp}@example.com`;
    const menteePassword = 'MenteeJourney123!';
    
    await menteeContext.goto('/signup');
    await menteeContext.fill('input[name="email"]', menteeEmail);
    await menteeContext.fill('input[name="password"]', menteePassword);
    await menteeContext.fill('input[name="confirmPassword"]', menteePassword);
    await menteeContext.fill('input[name="name"]', 'Journey Test Mentee');
    await menteeContext.selectOption('select[name="role"]', 'mentee');
    await menteeContext.fill('input[name="interests"]', 'Web Development, React');
    await menteeContext.fill('textarea[name="goals"]', 'Learn to build modern web applications and advance my career.');
    await menteeContext.click('button[type="submit"]');
    
    // Login mentee if redirected to login
    if (menteeContext.url().includes('/login')) {
      await menteeContext.fill('input[name="email"]', menteeEmail);
      await menteeContext.fill('input[name="password"]', menteePassword);
      await menteeContext.click('button[type="submit"]');
    }
    
    await expect(menteeContext).toHaveURL('/dashboard');
    await expect(menteeContext.locator('h1')).toContainText('Mentee Dashboard');
    
    // Step 3: Mentee browses and finds the mentor
    await menteeContext.click('[data-testid="browse-mentors-link"]');
    await expect(menteeContext).toHaveURL('/mentors');
    
    // Search for the mentor
    await menteeContext.fill('input[name="search"]', 'React');
    await menteeContext.click('[data-testid="search-button"]');
    
    // Find and click on our mentor
    const mentorCard = menteeContext.locator('[data-testid="mentor-card"]:has-text("Journey Test Mentor")');
    await expect(mentorCard).toBeVisible();
    await mentorCard.click();
    
    // Step 4: Send matching request
    await expect(menteeContext).toHaveURL(/\/mentors\/\d+/);
    await menteeContext.click('[data-testid="send-request-button"]');
    
    const requestMessage = 'Hi! I am very interested in learning full-stack development, especially React and Node.js. Your experience aligns perfectly with my learning goals. Would you be willing to mentor me?';
    await menteeContext.fill('textarea[name="message"]', requestMessage);
    await menteeContext.click('[data-testid="submit-request-button"]');
    
    await expect(menteeContext.locator('[data-testid="success-message"]')).toContainText('Request sent successfully');
    
    // Step 5: Mentor receives and reviews the request
    await page.reload();
    await expect(page.locator('[data-testid="pending-requests"]')).toContainText('1'); // Should show 1 pending request
    
    await page.click('[data-testid="view-requests-button"]');
    await expect(page).toHaveURL('/mentor/requests');
    
    // Verify request details
    const requestItem = page.locator('[data-testid="request-item"]');
    await expect(requestItem).toBeVisible();
    await expect(requestItem).toContainText('Journey Test Mentee');
    await expect(requestItem).toContainText(requestMessage);
    
    // Step 6: Mentor accepts the request
    await page.click('[data-testid="accept-request-button"]');
    await expect(page.locator('[data-testid="success-message"]')).toContainText('Request accepted');
    
    // Step 7: Verify mentorship is established
    await page.goto('/dashboard');
    await expect(page.locator('[data-testid="active-mentorships"]')).toContainText('1');
    
    // Step 8: Mentee sees the accepted status
    await menteeContext.goto('/mentee/requests');
    await expect(menteeContext.locator('[data-testid="request-status"]')).toContainText('accepted');
    
    await menteeContext.goto('/dashboard');
    await expect(menteeContext.locator('[data-testid="current-mentor"]')).toContainText('Journey Test Mentor');
    
    // Step 9: Test profile updates work for both users
    // Mentor updates profile
    await page.click('[data-testid="profile-link"]');
    await page.click('[data-testid="edit-profile-button"]');
    await page.fill('textarea[name="bio"]', 'Updated bio: Senior full-stack developer specializing in modern web technologies and mentoring.');
    await page.click('[data-testid="save-profile-button"]');
    await expect(page.locator('[data-testid="success-message"]')).toContainText('Profile updated');
    
    // Mentee updates profile
    await menteeContext.click('[data-testid="profile-link"]');
    await menteeContext.click('[data-testid="edit-profile-button"]');
    await menteeContext.fill('textarea[name="goals"]', 'Updated goals: Master React, Node.js, and cloud deployment to become a senior developer.');
    await menteeContext.click('[data-testid="save-profile-button"]');
    await expect(menteeContext.locator('[data-testid="success-message"]')).toContainText('Profile updated');
    
    // Step 10: Test logout functionality
    await page.click('[data-testid="user-menu"]');
    await page.click('[data-testid="logout-button"]');
    await expect(page).toHaveURL('/');
    await expect(page.locator('h2')).toContainText('로그인');
    
    await menteeContext.click('[data-testid="user-menu"]');
    await menteeContext.click('[data-testid="logout-button"]');
    await expect(menteeContext).toHaveURL('/');
    await expect(menteeContext.locator('h2')).toContainText('로그인');
    
    await menteeContext.close();
  });

  test('mentor can handle multiple requests', async ({ page, context }) => {
    const timestamp = Date.now();
    
    // Create mentor
    const mentorEmail = `multi_mentor_${timestamp}@example.com`;
    const mentorPassword = 'MultiMentor123!';
    
    await page.goto('/signup');
    await page.fill('input[name="email"]', mentorEmail);
    await page.fill('input[name="password"]', mentorPassword);
    await page.fill('input[name="confirmPassword"]', mentorPassword);
    await page.fill('input[name="name"]', 'Multi Request Mentor');
    await page.selectOption('select[name="role"]', 'mentor');
    await page.fill('input[name="expertise"]', 'Python, Django, Machine Learning');
    await page.fill('textarea[name="bio"]', 'Expert in Python and ML.');
    await page.click('button[type="submit"]');
    
    if (page.url().includes('/login')) {
      await page.fill('input[name="email"]', mentorEmail);
      await page.fill('input[name="password"]', mentorPassword);
      await page.click('button[type="submit"]');
    }
    
    // Create multiple mentees and send requests
    const menteeCount = 3;
    const menteePages = [];
    
    for (let i = 0; i < menteeCount; i++) {
      const menteePage = await context.newPage();
      const menteeEmail = `multi_mentee_${timestamp}_${i}@example.com`;
      const menteePassword = 'MultiMentee123!';
      
      await menteePage.goto('/signup');
      await menteePage.fill('input[name="email"]', menteeEmail);
      await menteePage.fill('input[name="password"]', menteePassword);
      await menteePage.fill('input[name="confirmPassword"]', menteePassword);
      await menteePage.fill('input[name="name"]', `Multi Test Mentee ${i + 1}`);
      await menteePage.selectOption('select[name="role"]', 'mentee');
      await menteePage.fill('input[name="interests"]', 'Python, Machine Learning');
      await menteePage.fill('textarea[name="goals"]', `Learning goals for mentee ${i + 1}.`);
      await menteePage.click('button[type="submit"]');
      
      if (menteePage.url().includes('/login')) {
        await menteePage.fill('input[name="email"]', menteeEmail);
        await menteePage.fill('input[name="password"]', menteePassword);
        await menteePage.click('button[type="submit"]');
      }
      
      // Send request to mentor
      await menteePage.goto('/mentors');
      await menteePage.click('[data-testid="mentor-card"]:has-text("Multi Request Mentor")');
      await menteePage.click('[data-testid="send-request-button"]');
      await menteePage.fill('textarea[name="message"]', `Request from mentee ${i + 1}.`);
      await menteePage.click('[data-testid="submit-request-button"]');
      
      menteePages.push(menteePage);
    }
    
    // Mentor should see all requests
    await page.reload();
    await expect(page.locator('[data-testid="pending-requests"]')).toContainText(menteeCount.toString());
    
    await page.click('[data-testid="view-requests-button"]');
    const requestItems = page.locator('[data-testid="request-item"]');
    await expect(requestItems).toHaveCount(menteeCount);
    
    // Accept first request, reject second, keep third pending
    await requestItems.nth(0).locator('[data-testid="accept-request-button"]').click();
    await expect(page.locator('[data-testid="success-message"]')).toContainText('Request accepted');
    
    await requestItems.nth(1).locator('[data-testid="reject-request-button"]').click();
    await expect(page.locator('[data-testid="success-message"]')).toContainText('Request rejected');
    
    // Verify dashboard shows correct counts
    await page.goto('/dashboard');
    await expect(page.locator('[data-testid="active-mentorships"]')).toContainText('1');
    await expect(page.locator('[data-testid="pending-requests"]')).toContainText('1');
    
    // Clean up
    for (const menteePage of menteePages) {
      await menteePage.close();
    }
  });
});
