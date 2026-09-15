"""Tests for dashboard ticker-universe selection behavior."""

from pathlib import Path
import sys
import unittest
from unittest.mock import patch

# Ensure repository root is on sys.path when executed directly as a script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.api_client import APIClientError
from src.universes import MARKET_UNIVERSES, get_ticker_options


class TestTickerUniverses(unittest.TestCase):
    """Verify the curated market universes exposed by the dashboard."""

    def test_expected_market_universes_are_available(self):
        self.assertTrue({"NIFTY 500", "Fortune 500"}.issubset(set(MARKET_UNIVERSES)))
        self.assertTrue(MARKET_UNIVERSES["NIFTY 500"])
        self.assertTrue(MARKET_UNIVERSES["Fortune 500"])
        self.assertIn("NASDAQ 100", MARKET_UNIVERSES)
        self.assertIn("BSE Sensex 30", MARKET_UNIVERSES)
        self.assertIn("FTSE 100 (UK)", MARKET_UNIVERSES)
        self.assertIn("DAX 40 (Germany)", MARKET_UNIVERSES)
        self.assertIn("Global Megacaps", MARKET_UNIVERSES)

    def test_universe_symbols_are_non_empty_and_unique(self):
        for symbols in MARKET_UNIVERSES.values():
            self.assertEqual(len(symbols), len(set(symbols)))
            self.assertTrue(all(symbol.strip() for symbol in symbols))
            self.assertTrue(all(symbol == symbol.upper() for symbol in symbols))

    def test_watchlist_keeps_available_symbol_order(self):
        available = ["MSFT", "AAPL", "MSFT"]

        self.assertEqual(get_ticker_options("My Watchlist", available), available)

    def test_universe_options_precede_custom_symbols_and_remove_duplicates(self):
        universe_symbols = MARKET_UNIVERSES["NIFTY 500"]
        available = ["CUSTOM", universe_symbols[0], "CUSTOM"]

        options = get_ticker_options("NIFTY 500", available)

        self.assertEqual(options[: len(universe_symbols)], list(universe_symbols))
        self.assertEqual(options[-1], "CUSTOM")
        self.assertEqual(len(options), len(set(options)))


class TestDashboardLoadPrices(unittest.TestCase):
    """Verify load_prices handles API errors by falling back to direct fetching."""

    def setUp(self):
        from src.dashboard import load_prices
        load_prices.clear()

    @patch("src.dashboard.fetch_quotes")
    def test_load_prices_uses_fastapi_when_reachable(self, mock_fetch):
        from src.dashboard import load_prices
        from src.tracker import StockQuote

        mock_fetch.return_value = {
            "AAPL": StockQuote(symbol="AAPL", name="Apple Inc.", price=150.0, currency="USD")
        }

        quotes, source = load_prices(("AAPL",))
        self.assertEqual(source, "FastAPI")
        self.assertIn("AAPL", quotes)

    @patch("src.dashboard.get_prices")
    @patch("src.dashboard.fetch_quotes", side_effect=APIClientError("unreachable"))
    def test_load_prices_falls_back_to_direct_when_api_unreachable(self, _mock_fetch, mock_get_prices):
        from src.dashboard import load_prices
        from src.tracker import StockQuote

        mock_get_prices.return_value = {
            "AAPL": StockQuote(symbol="AAPL", name="Apple Inc.", price=150.0, currency="USD")
        }

        quotes, source = load_prices(("AAPL",))
        self.assertEqual(source, "Direct")
        self.assertIn("AAPL", quotes)


class TestDashboardThemes(unittest.TestCase):
    """Verify modern theme palette availability and styling generation."""

    def test_theme_palettes_exceed_basic_light_and_dark(self):
        from src.themes import THEMES

        # Ensure more than just basic light and dark (at least 6 distinct themes)
        self.assertGreaterEqual(len(THEMES), 6)
        self.assertIn("Midnight Navy", THEMES)
        self.assertIn("Clean Light", THEMES)
        self.assertIn("Obsidian Noir", THEMES)
        self.assertIn("Emerald Wealth", THEMES)
        self.assertIn("Cyber Terminal", THEMES)
        self.assertIn("Sunset Horizon", THEMES)
        self.assertIn("Arctic Frost", THEMES)

    def test_theme_definitions_contain_required_tokens(self):
        from src.themes import THEMES

        for theme_name, theme in THEMES.items():
            self.assertEqual(theme.name, theme_name)
            self.assertTrue(theme.page_bg.startswith("#"))
            self.assertTrue(theme.accent_primary.startswith("#"))
            self.assertIn("gradient", theme.accent_gradient)
            self.assertTrue(theme.text_primary.startswith("#"))
            self.assertTrue(theme.surface_card.startswith("rgba"))

    def test_theme_resolution_and_aliases(self):
        from src.themes import resolve_theme

        # Test classic aliases
        dark_resolved = resolve_theme("Dark")
        self.assertEqual(dark_resolved.name, "Midnight Navy")

        light_resolved = resolve_theme("Light")
        self.assertEqual(light_resolved.name, "Clean Light")

        # Test direct resolution
        cyber_resolved = resolve_theme("Cyber Terminal")
        self.assertEqual(cyber_resolved.name, "Cyber Terminal")

        # Test fallback on None or invalid
        fallback_none = resolve_theme(None)
        self.assertEqual(fallback_none.name, "Midnight Navy")

        fallback_unknown = resolve_theme("NonExistentTheme")
        self.assertEqual(fallback_unknown.name, "Midnight Navy")

    def test_build_theme_css_contains_expected_variables(self):
        from src.themes import THEMES, build_theme_css

        for theme_name in THEMES:
            css = build_theme_css(theme_name)
            self.assertIn("<style>", css)
            self.assertIn("--ui-page:", css)
            self.assertIn("--ui-surface-card:", css)
            self.assertIn("--ui-hero-bg:", css)
            self.assertIn("--ui-accent-gradient:", css)
            self.assertIn("--ui-fab-gradient:", css)
            self.assertIn("data-testid=\"stMetric\"", css)
            self.assertIn("assistant_launcher", css)

    def test_build_theme_css_contains_chat_ui_tokens(self):
        from src.themes import build_theme_css

        css = build_theme_css("Midnight Navy")
        self.assertIn("stPopoverBody", css)
        self.assertIn("chat-header", css)
        self.assertIn("chat-context-bar", css)
        self.assertIn("chat-message-meta", css)
        self.assertIn("chat-footer-disclaimer", css)


if __name__ == "__main__":
    unittest.main()

