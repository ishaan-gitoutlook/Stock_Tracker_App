/**
 * 📘 Lesson 2.3 — Testing Your Stock Tracker Dashboard (ROBUST VERSION)
 *
 * LESSONS LEARNED (this is the 4th iteration!):
 *   1. Streamlit sidebars load AFTER main content — must wait explicitly
 *   2. Don't use 'networkidle' — Streamlit polls continuously
 *   3. Increase assertion timeouts for dynamic apps
 *   4. ARIA snapshot is your best debugging friend
 *
 * KEY TEACHING: Writing reliable tests for real apps is HARD.
 * This is exactly why AI + MCP is valuable — the AI can adapt
 * to timing issues and retry intelligently.
 *
 * Run:
 *   npx playwright test tests/e2e/03-stock-dashboard.spec.ts --headed
 */
import { test, expect, type Page } from '@playwright/test';

// Streamlit is heavy — give tests more time
test.setTimeout(60_000);

// ─── Helpers ─────────────────────────────────────────────────────

async function waitForStreamlitLoad(page: Page) {
  // Wait for DOM
  await page.waitForLoadState('domcontentloaded');

  // Wait for Streamlit's main container
  await page.locator('[data-testid="stAppViewContainer"]').waitFor({
    state: 'visible',
    timeout: 30_000,
  });

  // CRITICAL: Wait for the SIDEBAR to fully render too
  // The sidebar loads after the main content in Streamlit
  await page.locator('[data-testid="stSidebar"]').waitFor({
    state: 'visible',
    timeout: 15_000,
  });

  // Buffer for full React hydration of all widgets
  await page.waitForTimeout(4000);
}

// Longer timeout for Streamlit widget assertions
const WIDGET_TIMEOUT = 15_000;

// ─── Test Suite ──────────────────────────────────────────────────

test.describe('Stock Tracker Dashboard', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await waitForStreamlitLoad(page);
  });

  // ─── Test 1: App loads successfully ────────────────────────
  test('dashboard loads without errors', async ({ page }) => {
    const errorBanner = page.locator('[data-testid="stException"]');
    await expect(errorBanner).not.toBeVisible();
    await expect(page.locator('[data-testid="stAppViewContainer"]')).toBeVisible();
  });


  // ─── Test 2: Brand / Title is visible ──────────────────────
  test('StockPulse branding is visible', async ({ page }) => {
    const sidebar = page.locator('[data-testid="stSidebar"]');

    // Expand sidebar if collapsed
    if (!(await sidebar.isVisible())) {
      const toggle = page.locator('[data-testid="stSidebarCollapsedControl"]');
      if (await toggle.isVisible()) {
        await toggle.click();
        await sidebar.waitFor({ state: 'visible' });
      }
    }

    // Brand uses unsafe_allow_html — use CSS selector
    await expect(sidebar.locator('.brand-name')).toHaveText('StockPulse', { timeout: WIDGET_TIMEOUT });
    await expect(sidebar.locator('.brand-caption')).toHaveText('MARKET INTELLIGENCE');
  });


  // ─── Test 3: Sidebar has theme selector ────────────────────
  test('theme palette selector exists in sidebar', async ({ page }) => {
    const sidebar = page.locator('[data-testid="stSidebar"]');

    // Streamlit selectboxes use data-testid="stSelectbox"
    // Check for the selectbox widget itself (more reliable than label text)
    await expect(
      sidebar.locator('[data-testid="stSelectbox"]').first()
    ).toBeVisible({ timeout: WIDGET_TIMEOUT });
  });


  // ─── Test 4: Stock listing header ──────────────────────────
  test('stock listings header is present', async ({ page }) => {
    const sidebar = page.locator('[data-testid="stSidebar"]');

    // Look for the header using Streamlit's header testid
    await expect(
      sidebar.getByText('Stock Listings', { exact: false })
    ).toBeVisible({ timeout: WIDGET_TIMEOUT });
  });


  // ─── Test 5: Quick preset buttons exist ────────────────────
  test('quick preset buttons are available', async ({ page }) => {
    const sidebar = page.locator('[data-testid="stSidebar"]');

    // Scroll down in sidebar to reveal buttons
    await sidebar.locator('[data-testid="stSidebarContent"]').evaluate(
      el => el.scrollTop = el.scrollHeight / 3
    );
    await page.waitForTimeout(500);

    // Streamlit buttons use data-testid="stBaseButton-secondary"
    // Find buttons by their inner paragraph text
    const sidebarButtons = sidebar.locator('[data-testid="stBaseButton-secondary"]');
    await expect(sidebarButtons.first()).toBeVisible({ timeout: WIDGET_TIMEOUT });

    // Verify we have at least 3 preset buttons (Top 4, Top 8, All)
    const count = await sidebarButtons.count();
    expect(count).toBeGreaterThanOrEqual(3);
  });


  // ─── Test 6: Screenshot test ───────────────────────────────
  test('capture dashboard screenshot', async ({ page }) => {
    await page.screenshot({
      path: 'tests/e2e/screenshots/dashboard-initial.png',
      fullPage: true,
    });
  });


  // ─── Test 7: ARIA Snapshot (Module 3 preview) ──────────────
  // 🔮 This is what the AI "sees" via MCP!
  test('preview: dump ARIA snapshot (what AI sees via MCP)', async ({ page }) => {
    const snapshot = await page.locator('body').ariaSnapshot();

    console.log('\n' + '='.repeat(60));
    console.log('🔮 ARIA SNAPSHOT — What the AI sees via MCP');
    console.log('='.repeat(60));
    console.log(snapshot.substring(0, 3000));
    console.log('... (truncated for readability)');
    console.log('='.repeat(60));

    expect(snapshot.length).toBeGreaterThan(0);
    expect(snapshot).toContain('button');
  });
});
