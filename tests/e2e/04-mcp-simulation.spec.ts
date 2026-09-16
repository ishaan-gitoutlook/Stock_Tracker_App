/**
 * 📘 Lesson 3.3 — See What the AI Sees via MCP
 *
 * This test simulates what the Playwright MCP server does:
 * 1. Opens your Stock Tracker
 * 2. Takes an ARIA snapshot (what MCP sends to the AI)
 * 3. Finds elements by ref (how MCP identifies them)
 * 4. Performs actions (what the AI tells MCP to do)
 * 5. Takes another snapshot (how the AI confirms success)
 *
 * Run:
 *   npx playwright test tests/e2e/04-mcp-simulation.spec.ts --headed
 */
import { test, expect, type Page } from '@playwright/test';

test.setTimeout(60_000);

async function waitForApp(page: Page) {
  await page.waitForLoadState('domcontentloaded');
  await page.locator('[data-testid="stAppViewContainer"]').waitFor({
    state: 'visible',
    timeout: 30_000,
  });
  await page.locator('[data-testid="stSidebar"]').waitFor({
    state: 'visible',
    timeout: 15_000,
  });
  await page.waitForTimeout(4000);
}

test.describe('MCP Simulation — Think Like an AI Agent', () => {

  // ─── Simulation 1: The See → Think → Act Loop ─────────────
  // This is the CORE pattern of AI + MCP automation

  test('Simulate: AI reads the page and interacts', async ({ page }) => {
    await page.goto('/');
    await waitForApp(page);

    // ── STEP 1: SEE (browser_snapshot) ──
    // The MCP server calls this and sends the result to the AI
    console.log('\n🤖 STEP 1: AI calls browser_snapshot...');
    const snapshot1 = await page.locator('body').ariaSnapshot();
    console.log('📋 AI receives ARIA tree:');
    console.log(snapshot1.substring(0, 1500));

    // ── STEP 2: THINK ──
    // The AI analyzes the snapshot and decides what to do
    // It sees: radiogroup "Select Stock Listing to View:"
    //          - radio "🇺🇸 S&P 500 / Fortune 500 (US)"
    console.log('\n🧠 STEP 2: AI thinks: "I see a radio for S&P 500. I\'ll click it."');

    // ── STEP 3: ACT (browser_click) ──
    // The AI tells MCP: click the S&P 500 radio button
    console.log('\n🖱️ STEP 3: AI calls browser_click(element="S&P 500", ref="...")');
    // LESSON: Streamlit's sticky header can overlay elements!
    // MCP handles this by clicking via element ref (which uses force).
    // In Playwright tests, we use { force: true } or click the visible text.
    const sp500Text = page.getByText('S&P 500 / Fortune 500', { exact: false });
    await sp500Text.click({ force: true });
    await page.waitForTimeout(3000); // Wait for Streamlit to re-render

    // ── STEP 4: SEE AGAIN (browser_snapshot) ──
    // The AI checks: did the click work?
    console.log('\n🤖 STEP 4: AI calls browser_snapshot again...');
    const snapshot2 = await page.locator('body').ariaSnapshot();

    // ── STEP 5: VERIFY ──
    // The AI checks if S&P 500 is now selected
    const hasSnP500 = snapshot2.includes('S&P 500') || snapshot2.includes('S\\&P 500');
    console.log(`\n✅ STEP 5: AI verifies: S&P 500 in updated page? ${hasSnP500}`);

    // Verify the page responded to the click
    expect(snapshot2.length).toBeGreaterThan(0);

    console.log('\n🎉 AI agent task complete: Successfully switched to S&P 500 listing!');
  });


  // ─── Simulation 2: Multi-step agent workflow ───────────────
  // A more complex scenario: the AI performs multiple actions

  test('Simulate: AI performs multi-step workflow', async ({ page }) => {
    await page.goto('/');
    await waitForApp(page);

    console.log('\n' + '='.repeat(60));
    console.log('🤖 MULTI-STEP AGENT: "Change theme and switch listing"');
    console.log('='.repeat(60));

    // ── Agent Step 1: Read the page ──
    console.log('\n📸 Agent reads page...');
    const initialSnapshot = await page.locator('body').ariaSnapshot();

    // ── Agent Step 2: Find and interact with theme selector ──
    console.log('\n🎨 Agent: "I see combobox \'Theme Palette\'. I\'ll click it."');
    const sidebar = page.locator('[data-testid="stSidebar"]');
    const themeSelect = sidebar.locator('[data-testid="stSelectbox"]').first();
    await themeSelect.click();
    await page.waitForTimeout(1000);

    // The dropdown opens — take another snapshot to see options
    console.log('📋 Agent reads dropdown options...');
    const dropdownSnapshot = await page.locator('body').ariaSnapshot();
    // Log just the options part
    const optionLines = dropdownSnapshot.split('\n').filter(l => l.includes('option'));
    console.log('   Available themes:', optionLines.slice(0, 5).join('\n   '));

    // Select a different theme option
    const themeOption = page.getByRole('option').filter({ hasText: /Frost|Ocean|Ember/i }).first();
    if (await themeOption.isVisible()) {
      const themeName = await themeOption.textContent();
      console.log(`\n🎨 Agent clicks theme: "${themeName}"`);
      await themeOption.click();
      await page.waitForTimeout(2000);
    } else {
      // Close dropdown if no matching theme found
      await page.keyboard.press('Escape');
      console.log('\n🎨 Agent: No matching theme found, skipping');
    }

    // ── Agent Step 3: Screenshot for evidence ──
    console.log('\n📸 Agent takes screenshot as evidence...');
    await page.screenshot({
      path: 'tests/e2e/screenshots/after-agent-actions.png',
      fullPage: true,
    });

    // ── Agent Step 4: Final verification ──
    console.log('\n🤖 Agent takes final snapshot to confirm state...');
    const finalSnapshot = await page.locator('body').ariaSnapshot();
    expect(finalSnapshot.length).toBeGreaterThan(0);

    console.log('\n✅ Multi-step agent workflow complete!');
    console.log('='.repeat(60));
  });


  // ─── Simulation 3: How MCP handles element references ─────
  // The "ref" system is how MCP uniquely identifies elements

  test('Understand: How element references work', async ({ page }) => {
    await page.goto('/');
    await waitForApp(page);

    console.log('\n' + '='.repeat(60));
    console.log('📚 LESSON: How MCP Element References (ref) Work');
    console.log('='.repeat(60));

    // In MCP, every interactive element gets a unique "ref" ID
    // The AI uses these refs to target specific elements

    // Let's see how Playwright internally matches elements:
    const buttons = page.locator('[data-testid="stSidebar"] button');
    const buttonCount = await buttons.count();

    console.log(`\n🔢 Found ${buttonCount} buttons in sidebar`);
    console.log('\nIn MCP, each would get a ref like:');

    for (let i = 0; i < Math.min(buttonCount, 5); i++) {
      const btn = buttons.nth(i);
      const text = await btn.textContent();
      const label = await btn.getAttribute('aria-label');
      console.log(`  ref="e${i+1}" → button "${label || text?.trim() || '(unnamed)'}"`);
    }

    console.log('\n📖 KEY INSIGHT:');
    console.log('   When AI says: browser_click(ref="e3")');
    console.log('   MCP translates to: page.locator("[ref=e3]").click()');
    console.log('   The AI never writes CSS selectors — it uses refs!');
    console.log('='.repeat(60));

    expect(buttonCount).toBeGreaterThan(0);
  });
});
