/**
 * 📘 Lesson 2.3 — Testing Your Stock Tracker Dashboard
 *
 * Now we apply everything from Lessons 2.1 and 2.2 to YOUR real app.
 * This is a Streamlit app (StockPulse), so we'll learn Streamlit-specific
 * locator patterns too.
 *
 * KEY INSIGHT: Streamlit renders custom HTML with specific patterns.
 * The accessibility tree for Streamlit widgets is different from plain HTML.
 * This is EXACTLY the kind of discovery you'll need when using MCP on
 * real-world apps!
 *
 * Prerequisites: App running on http://localhost:8501
 *   Start with: .venv\Scripts\python.exe -m streamlit run main.py
 *
 * Run:
 *   npx playwright test tests/e2e/03-stock-dashboard.spec.ts --headed
 */
import { test, expect, type Page } from '@playwright/test';

// ─── Helpers ─────────────────────────────────────────────────────
// Streamlit apps take a moment to hydrate. This helper waits for the
// app to be fully loaded before tests interact with it.

async function waitForStreamlitLoad(page: Page) {
  // Streamlit shows a loading spinner initially — wait for it to disappear
  // Then wait for the main content to be stable
  await page.waitForLoadState('networkidle');
  // Give Streamlit extra time to hydrate its React components
  await page.waitForTimeout(2000);
}

// ─── Test Suite ──────────────────────────────────────────────────

test.describe('Stock Tracker Dashboard', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto('/');  // Uses baseURL from playwright.config.ts
    await waitForStreamlitLoad(page);
  });

  // ─── Test 1: App loads successfully ────────────────────────
  // The most basic test — does the page load at all?
  test('dashboard loads without errors', async ({ page }) => {
    // Streamlit error messages have a specific pattern
    // If the app crashes, Streamlit shows an error banner
    const errorBanner = page.locator('[data-testid="stException"]');
    await expect(errorBanner).not.toBeVisible();

    // The app should have some content (not a blank page)
    await expect(page.locator('body')).not.toBeEmpty();
  });


  // ─── Test 2: Brand / Title is visible ──────────────────────
  // Check that the StockPulse branding renders
  test('StockPulse branding is visible', async ({ page }) => {
    // The sidebar brand "StockPulse" should be present
    // Using getByText — a reliable way to find visible text
    await expect(page.getByText('StockPulse')).toBeVisible();
    await expect(page.getByText('MARKET INTELLIGENCE')).toBeVisible();
  });


  // ─── Test 3: Sidebar has theme selector ────────────────────
  // Streamlit selectboxes render as custom dropdowns
  test('theme palette selector exists in sidebar', async ({ page }) => {
    // Streamlit sidebar has a specific test-id
    const sidebar = page.locator('[data-testid="stSidebar"]');
    await expect(sidebar).toBeVisible();

    // The Theme Palette selectbox — Streamlit labels its selectboxes
    await expect(sidebar.getByText('Theme Palette')).toBeVisible();
  });


  // ─── Test 4: Stock listing selector works ──────────────────
  // The sidebar has a "Select Market Listing" dropdown
  test('market listing selector is present', async ({ page }) => {
    const sidebar = page.locator('[data-testid="stSidebar"]');

    // Check the listing section header
    await expect(sidebar.getByText('Stock Listings & Exchanges')).toBeVisible();

    // Check the select dropdown exists
    await expect(sidebar.getByText('Select Market Listing')).toBeVisible();
  });


  // ─── Test 5: Quick preset buttons exist ────────────────────
  // The sidebar has Top 4, Top 8, All buttons
  test('quick preset buttons are available', async ({ page }) => {
    const sidebar = page.locator('[data-testid="stSidebar"]');

    // Check all three preset buttons
    await expect(sidebar.getByRole('button', { name: 'Top 4' })).toBeVisible();
    await expect(sidebar.getByRole('button', { name: 'Top 8' })).toBeVisible();
    await expect(sidebar.getByRole('button', { name: 'All' })).toBeVisible();
  });


  // ─── Test 6: Screenshot test (visual documentation) ────────
  // Capture how your app looks — useful for visual regression later
  test('capture dashboard screenshot', async ({ page }) => {
    await page.screenshot({
      path: 'tests/e2e/screenshots/dashboard-initial.png',
      fullPage: true,
    });

    // Verify the screenshot was taken (file exists is implicit)
    // This also serves as documentation of what the app looks like!
  });


  // ─── Test 7: Page accessibility snapshot ───────────────────
  // 🔮 PREVIEW OF MODULE 3: This is what the AI will "see" via MCP!
  test('preview: dump accessibility tree (what AI sees)', async ({ page }) => {
    // This is the accessibility snapshot — the EXACT data MCP sends to the AI
    const snapshot = await page.accessibility.snapshot();

    console.log('\n' + '='.repeat(60));
    console.log('🔮 ACCESSIBILITY TREE — What the AI sees via MCP');
    console.log('='.repeat(60));
    console.log(JSON.stringify(snapshot, null, 2).substring(0, 3000));
    console.log('... (truncated for readability)');
    console.log('='.repeat(60));

    // The snapshot should not be null (page has accessible content)
    expect(snapshot).not.toBeNull();
  });
});
