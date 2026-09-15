/**
 * 📘 Lesson 2.1 — Your First Playwright Test
 *
 * What you'll learn:
 *   1. test() — defines a test case (like def test_xxx in pytest)
 *   2. page.goto() — navigates to a URL
 *   3. expect() — makes assertions
 *   4. page.getByRole() — finds elements by accessibility role
 *
 * Run this test:
 *   npx playwright test tests/e2e/01-hello-world.spec.ts --headed
 *
 * The --headed flag opens a visible browser so you can WATCH what happens!
 */
import { test, expect } from '@playwright/test';

// ─── Test 1: Navigate and check the title ────────────────────────
// This is the absolute simplest Playwright test.
// Think of it as "open a browser, go to a URL, check the title".

test('Playwright.dev has the correct title', async ({ page }) => {
  // Step 1: Navigate (like typing a URL in the address bar)
  await page.goto('https://playwright.dev/');

  // Step 2: Assert the page title
  // expect() + toHaveTitle() checks the <title> tag
  await expect(page).toHaveTitle(/Playwright/);
});


// ─── Test 2: Click a link and verify navigation ──────────────────
// Now let's interact! We'll click a link and check where it goes.

test('Can navigate to the Getting Started page', async ({ page }) => {
  await page.goto('https://playwright.dev/');

  // Step 1: Find the "Get started" link using getByRole()
  // getByRole('link') looks for <a> tags — an ACCESSIBILITY role
  // { name: 'Get started' } matches the visible text
  const getStartedLink = page.getByRole('link', { name: 'Get started' });

  // Step 2: Click it
  await getStartedLink.click();

  // Step 3: Verify we landed on the right page
  // toHaveURL() checks the browser URL contains this text
  await expect(page).toHaveURL(/.*intro/);
});


// ─── Test 3: Search and check results ────────────────────────────
// A more realistic test — using a search box.

test('Search returns results', async ({ page }) => {
  await page.goto('https://playwright.dev/');

  // Step 1: Click the search button (Playwright.dev uses a search button)
  // Notice: getByRole('button') — another accessibility role!
  await page.getByRole('button', { name: 'Search' }).click();

  // Step 2: Type into the search dialog
  // getByPlaceholder() finds by placeholder text — another common pattern
  const searchInput = page.getByPlaceholder('Search docs');
  await searchInput.fill('locators');

  // Step 3: Wait for and check results
  // getByRole('link') finds links in the search results
  await expect(page.getByRole('link', { name: /Locators/ }).first()).toBeVisible();
});
