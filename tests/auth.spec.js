import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should load the login page', async ({ page }) => {
    await expect(page).toHaveTitle(/Mentor-Mentee/);
    await expect(page.locator('h2')).toContainText('로그인');
    await expect(page.locator('input[name="email"]')).toBeVisible();
    await expect(page.locator('input[name="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('should show validation errors for empty fields', async ({ page }) => {
    await page.click('button[type="submit"]');
    
    // Check for HTML5 validation or custom error messages
    const emailInput = page.locator('input[name="email"]');
    const passwordInput = page.locator('input[name="password"]');
    
    await expect(emailInput).toHaveAttribute('required');
    await expect(passwordInput).toHaveAttribute('required');
  });

  test('should navigate to signup page', async ({ page }) => {
    await page.click('a[href="/signup"]');
    await expect(page).toHaveURL('/signup');
    await expect(page.locator('h2')).toContainText('회원가입');
  });

  test('should perform successful user registration', async ({ page }) => {
    await page.goto('/signup');
    
    const timestamp = Date.now();
    const testEmail = `test${timestamp}@example.com`;
    const testPassword = 'TestPassword123!';
    
    // Fill signup form
    await page.fill('input[name="email"]', testEmail);
    await page.fill('input[name="password"]', testPassword);
    await page.fill('input[name="confirmPassword"]', testPassword);
    await page.fill('input[name="name"]', 'Test User');
    await page.selectOption('select[name="role"]', 'mentee');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Should redirect to login or dashboard
    await expect(page).toHaveURL(/\/(login|dashboard)/);
  });

  test('should perform successful login', async ({ page }) => {
    // First create a user (this assumes the signup test passed)
    const timestamp = Date.now();
    const testEmail = `login${timestamp}@example.com`;
    const testPassword = 'TestPassword123!';
    
    // Register user first
    await page.goto('/signup');
    await page.fill('input[name="email"]', testEmail);
    await page.fill('input[name="password"]', testPassword);
    await page.fill('input[name="confirmPassword"]', testPassword);
    await page.fill('input[name="name"]', 'Login Test User');
    await page.selectOption('select[name="role"]', 'mentee');
    await page.click('button[type="submit"]');
    
    // Now test login
    await page.goto('/');
    await page.fill('input[name="email"]', testEmail);
    await page.fill('input[name="password"]', testPassword);
    await page.click('button[type="submit"]');
    
    // Should redirect to dashboard
    await expect(page).toHaveURL('/dashboard');
    
    // Check if user is logged in
    await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.fill('input[name="email"]', 'invalid@example.com');
    await page.fill('input[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');
    
    // Check for error message
    await expect(page.locator('[data-testid="error-message"]')).toContainText('Invalid credentials');
  });

  test('should logout successfully', async ({ page }) => {
    // Login first
    const timestamp = Date.now();
    const testEmail = `logout${timestamp}@example.com`;
    const testPassword = 'TestPassword123!';
    
    await page.goto('/signup');
    await page.fill('input[name="email"]', testEmail);
    await page.fill('input[name="password"]', testPassword);
    await page.fill('input[name="confirmPassword"]', testPassword);
    await page.fill('input[name="name"]', 'Logout Test User');
    await page.selectOption('select[name="role"]', 'mentee');
    await page.click('button[type="submit"]');
    
    await page.goto('/');
    await page.fill('input[name="email"]', testEmail);
    await page.fill('input[name="password"]', testPassword);
    await page.click('button[type="submit"]');
    
    // Logout
    await page.click('[data-testid="user-menu"]');
    await page.click('[data-testid="logout-button"]');
    
    // Should redirect to login
    await expect(page).toHaveURL('/');
    await expect(page.locator('h2')).toContainText('로그인');
  });
});
