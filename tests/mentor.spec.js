import { test, expect } from '@playwright/test';

test.describe('Mentor Features', () => {
  let mentorEmail, mentorPassword;

  test.beforeAll(async () => {
    const timestamp = Date.now();
    mentorEmail = `mentor${timestamp}@example.com`;
    mentorPassword = 'MentorPassword123!';
  });

  test.beforeEach(async ({ page }) => {
    // Register and login as mentor
    await page.goto('/signup');
    await page.fill('input[name="email"]', mentorEmail);
    await page.fill('input[name="password"]', mentorPassword);
    await page.fill('input[name="confirmPassword"]', mentorPassword);
    await page.fill('input[name="name"]', 'Test Mentor');
    await page.selectOption('select[name="role"]', 'mentor');
    await page.fill('input[name="expertise"]', 'JavaScript, React, Node.js');
    await page.fill('textarea[name="bio"]', 'Experienced software developer with 5+ years in web development.');
    await page.click('button[type="submit"]');
    
    // Login
    await page.goto('/');
    await page.fill('input[name="email"]', mentorEmail);
    await page.fill('input[name="password"]', mentorPassword);
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL('/dashboard');
  });

  test('should display mentor dashboard', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Mentor Dashboard');
    await expect(page.locator('[data-testid="pending-requests"]')).toBeVisible();
    await expect(page.locator('[data-testid="active-mentorships"]')).toBeVisible();
  });

  test('should view and manage matching requests', async ({ page }) => {
    await page.click('[data-testid="view-requests-button"]');
    await expect(page).toHaveURL('/mentor/requests');
    
    // Check if requests are displayed
    await expect(page.locator('[data-testid="requests-list"]')).toBeVisible();
  });

  test('should accept a matching request', async ({ page }) => {
    // Create a mentee first and send a request
    const menteeTimestamp = Date.now();
    const menteeEmail = `mentee${menteeTimestamp}@example.com`;
    
    // Open new page for mentee registration
    const menteeContext = await page.context().newPage();
    await menteeContext.goto('/signup');
    await menteeContext.fill('input[name="email"]', menteeEmail);
    await menteeContext.fill('input[name="password"]', 'MenteePassword123!');
    await menteeContext.fill('input[name="confirmPassword"]', 'MenteePassword123!');
    await menteeContext.fill('input[name="name"]', 'Test Mentee');
    await menteeContext.selectOption('select[name="role"]', 'mentee');
    await menteeContext.fill('input[name="interests"]', 'Web Development, JavaScript');
    await menteeContext.click('button[type="submit"]');
    
    // Login as mentee
    await menteeContext.goto('/');
    await menteeContext.fill('input[name="email"]', menteeEmail);
    await menteeContext.fill('input[name="password"]', 'MenteePassword123!');
    await menteeContext.click('button[type="submit"]');
    
    // Send matching request
    await menteeContext.goto('/mentors');
    await menteeContext.click('[data-testid="send-request-button"]');
    await menteeContext.fill('textarea[name="message"]', 'I would like to learn web development from you.');
    await menteeContext.click('[data-testid="submit-request-button"]');
    
    await menteeContext.close();
    
    // Back to mentor view
    await page.reload();
    await page.click('[data-testid="view-requests-button"]');
    
    // Accept the request
    await expect(page.locator('[data-testid="request-item"]')).toBeVisible();
    await page.click('[data-testid="accept-request-button"]');
    
    // Verify acceptance
    await expect(page.locator('[data-testid="success-message"]')).toContainText('Request accepted');
  });

  test('should update mentor profile', async ({ page }) => {
    await page.click('[data-testid="profile-link"]');
    await expect(page).toHaveURL('/profile');
    
    await page.click('[data-testid="edit-profile-button"]');
    await page.fill('textarea[name="bio"]', 'Updated bio: Senior full-stack developer specializing in modern web technologies.');
    await page.fill('input[name="expertise"]', 'JavaScript, React, Node.js, Python, AWS');
    await page.click('[data-testid="save-profile-button"]');
    
    await expect(page.locator('[data-testid="success-message"]')).toContainText('Profile updated');
  });
});
