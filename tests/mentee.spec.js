import { test, expect } from '@playwright/test';

test.describe('Mentee Features', () => {
  let menteeEmail, menteePassword;

  test.beforeAll(async () => {
    const timestamp = Date.now();
    menteeEmail = `mentee${timestamp}@example.com`;
    menteePassword = 'MenteePassword123!';
  });

  test.beforeEach(async ({ page }) => {
    // Register and login as mentee
    await page.goto('/signup');
    await page.fill('input[name="email"]', menteeEmail);
    await page.fill('input[name="password"]', menteePassword);
    await page.fill('input[name="confirmPassword"]', menteePassword);
    await page.fill('input[name="name"]', 'Test Mentee');
    await page.selectOption('select[name="role"]', 'mentee');
    await page.fill('input[name="interests"]', 'Web Development, Machine Learning');
    await page.fill('textarea[name="goals"]', 'Learn full-stack development and build a portfolio.');
    await page.click('button[type="submit"]');
    
    // Login
    await page.goto('/');
    await page.fill('input[name="email"]', menteeEmail);
    await page.fill('input[name="password"]', menteePassword);
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL('/dashboard');
  });

  test('should display mentee dashboard', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Mentee Dashboard');
    await expect(page.locator('[data-testid="current-mentor"]')).toBeVisible();
    await expect(page.locator('[data-testid="request-status"]')).toBeVisible();
  });

  test('should browse available mentors', async ({ page }) => {
    await page.click('[data-testid="browse-mentors-link"]');
    await expect(page).toHaveURL('/mentors');
    
    await expect(page.locator('h1')).toContainText('Available Mentors');
    await expect(page.locator('[data-testid="mentors-grid"]')).toBeVisible();
  });

  test('should filter mentors by expertise', async ({ page }) => {
    await page.goto('/mentors');
    
    await page.fill('input[name="search"]', 'JavaScript');
    await page.click('[data-testid="search-button"]');
    
    // Verify filtered results
    const mentorCards = page.locator('[data-testid="mentor-card"]');
    await expect(mentorCards.first()).toBeVisible();
    
    // Check if mentor expertise contains JavaScript
    await expect(mentorCards.first().locator('[data-testid="mentor-expertise"]')).toContainText('JavaScript');
  });

  test('should send matching request to mentor', async ({ page }) => {
    // First create a mentor
    const mentorTimestamp = Date.now();
    const mentorEmail = `targetmentor${mentorTimestamp}@example.com`;
    
    const mentorContext = await page.context().newPage();
    await mentorContext.goto('/signup');
    await mentorContext.fill('input[name="email"]', mentorEmail);
    await mentorContext.fill('input[name="password"]', 'MentorPassword123!');
    await mentorContext.fill('input[name="confirmPassword"]', 'MentorPassword123!');
    await mentorContext.fill('input[name="name"]', 'Target Mentor');
    await mentorContext.selectOption('select[name="role"]', 'mentor');
    await mentorContext.fill('input[name="expertise"]', 'React, TypeScript');
    await mentorContext.fill('textarea[name="bio"]', 'Expert React developer.');
    await mentorContext.click('button[type="submit"]');
    await mentorContext.close();
    
    // Browse mentors and send request
    await page.goto('/mentors');
    await page.click('[data-testid="mentor-card"]:has-text("Target Mentor")');
    
    await expect(page).toHaveURL(/\/mentors\/\d+/);
    await page.click('[data-testid="send-request-button"]');
    
    // Fill request form
    await page.fill('textarea[name="message"]', 'I am interested in learning React and TypeScript. Would you be willing to mentor me?');
    await page.click('[data-testid="submit-request-button"]');
    
    await expect(page.locator('[data-testid="success-message"]')).toContainText('Request sent successfully');
  });

  test('should view request status', async ({ page }) => {
    await page.click('[data-testid="my-requests-link"]');
    await expect(page).toHaveURL('/mentee/requests');
    
    await expect(page.locator('[data-testid="requests-list"]')).toBeVisible();
    await expect(page.locator('[data-testid="request-status"]')).toBeVisible();
  });

  test('should update mentee profile', async ({ page }) => {
    await page.click('[data-testid="profile-link"]');
    await expect(page).toHaveURL('/profile');
    
    await page.click('[data-testid="edit-profile-button"]');
    await page.fill('input[name="interests"]', 'Full-Stack Development, DevOps, Cloud Computing');
    await page.fill('textarea[name="goals"]', 'Build production-ready applications and deploy them to cloud platforms.');
    await page.click('[data-testid="save-profile-button"]');
    
    await expect(page.locator('[data-testid="success-message"]')).toContainText('Profile updated');
  });

  test('should cancel a pending request', async ({ page }) => {
    // Send a request first (reuse the mentor creation logic)
    const mentorTimestamp = Date.now();
    const mentorEmail = `cancelmentor${mentorTimestamp}@example.com`;
    
    const mentorContext = await page.context().newPage();
    await mentorContext.goto('/signup');
    await mentorContext.fill('input[name="email"]', mentorEmail);
    await mentorContext.fill('input[name="password"]', 'MentorPassword123!');
    await mentorContext.fill('input[name="confirmPassword"]', 'MentorPassword123!');
    await mentorContext.fill('input[name="name"]', 'Cancel Test Mentor');
    await mentorContext.selectOption('select[name="role"]', 'mentor');
    await mentorContext.fill('input[name="expertise"]', 'Vue.js');
    await mentorContext.fill('textarea[name="bio"]', 'Vue.js expert.');
    await mentorContext.click('button[type="submit"]');
    await mentorContext.close();
    
    // Send request
    await page.goto('/mentors');
    await page.click('[data-testid="mentor-card"]:has-text("Cancel Test Mentor")');
    await page.click('[data-testid="send-request-button"]');
    await page.fill('textarea[name="message"]', 'Test request to be cancelled.');
    await page.click('[data-testid="submit-request-button"]');
    
    // Go to requests and cancel
    await page.goto('/mentee/requests');
    await page.click('[data-testid="cancel-request-button"]');
    
    await expect(page.locator('[data-testid="success-message"]')).toContainText('Request cancelled');
  });
});
