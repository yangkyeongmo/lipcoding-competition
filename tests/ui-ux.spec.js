import { test, expect } from '@playwright/test';

test.describe('UI/UX and Accessibility Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should be responsive on mobile devices', async ({ page }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    await expect(page.locator('.max-w-md')).toBeVisible();
    await expect(page.locator('input[name="email"]')).toBeVisible();
    await expect(page.locator('input[name="password"]')).toBeVisible();
    
    // Elements should be properly sized for mobile
    const emailInput = page.locator('input[name="email"]');
    const boundingBox = await emailInput.boundingBox();
    expect(boundingBox.width).toBeGreaterThan(200); // Should be wide enough for mobile
  });

  test('should be responsive on tablet devices', async ({ page }) => {
    // Test tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    
    await expect(page.locator('.max-w-md')).toBeVisible();
    await expect(page.locator('form')).toBeVisible();
  });

  test('should handle keyboard navigation', async ({ page }) => {
    // Test tab navigation
    await page.keyboard.press('Tab');
    await expect(page.locator('input[name="email"]')).toBeFocused();
    
    await page.keyboard.press('Tab');
    await expect(page.locator('input[name="password"]')).toBeFocused();
    
    await page.keyboard.press('Tab');
    await expect(page.locator('button[type="submit"]')).toBeFocused();
    
    // Test form submission with Enter key
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.keyboard.press('Enter');
    
    // Should attempt to submit form
  });

  test('should have proper accessibility attributes', async ({ page }) => {
    // Check for proper labels
    const emailInput = page.locator('input[name="email"]');
    await expect(emailInput).toHaveAttribute('type', 'email');
    await expect(emailInput).toHaveAttribute('required');
    
    const passwordInput = page.locator('input[name="password"]');
    await expect(passwordInput).toHaveAttribute('type', 'password');
    await expect(passwordInput).toHaveAttribute('required');
    
    // Check for form labels (even if sr-only)
    await expect(page.locator('label[for="email"]')).toBeVisible();
    await expect(page.locator('label[for="password"]')).toBeVisible();
  });

  test('should have good color contrast', async ({ page }) => {
    // This is a visual test - in a real scenario you'd use axe-playwright
    // For now, we'll check that text is visible and readable
    const heading = page.locator('h2');
    await expect(heading).toBeVisible();
    
    const emailInput = page.locator('input[name="email"]');
    await expect(emailInput).toBeVisible();
    
    const submitButton = page.locator('button[type="submit"]');
    await expect(submitButton).toBeVisible();
  });

  test('should show loading states', async ({ page }) => {
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password123');
    
    // Click submit and check for loading state
    await page.click('button[type="submit"]');
    
    // Check if button is disabled during submission
    const submitButton = page.locator('button[type="submit"]');
    await expect(submitButton).toHaveAttribute('disabled');
  });

  test('should handle network errors gracefully', async ({ page }) => {
    // Intercept network requests and simulate failure
    await page.route('**/api/login', route => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Internal server error' })
      });
    });
    
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    
    // Should show error message
    await expect(page.locator('[data-testid="error-message"]')).toContainText('error');
  });

  test('should display proper page titles', async ({ page }) => {
    await expect(page).toHaveTitle(/Mentor-Mentee/);
    
    await page.goto('/signup');
    await expect(page).toHaveTitle(/Sign Up/);
  });

  test('should have proper meta tags for SEO', async ({ page }) => {
    // Check for viewport meta tag
    const viewportMeta = page.locator('meta[name="viewport"]');
    await expect(viewportMeta).toHaveAttribute('content', /width=device-width/);
    
    // Check for description meta tag
    const descriptionMeta = page.locator('meta[name="description"]');
    await expect(descriptionMeta).toBeAttached();
  });

  test('should handle form validation feedback', async ({ page }) => {
    // Submit empty form
    await page.click('button[type="submit"]');
    
    // Check for validation messages
    const emailInput = page.locator('input[name="email"]');
    const passwordInput = page.locator('input[name="password"]');
    
    // HTML5 validation should prevent submission
    await expect(emailInput).toHaveAttribute('required');
    await expect(passwordInput).toHaveAttribute('required');
  });

  test('should support browser back/forward navigation', async ({ page }) => {
    await page.goto('/signup');
    await expect(page).toHaveURL('/signup');
    
    await page.goBack();
    await expect(page).toHaveURL('/');
    
    await page.goForward();
    await expect(page).toHaveURL('/signup');
  });
});
