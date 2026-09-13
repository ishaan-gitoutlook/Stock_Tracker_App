"""Tests for dashboard ticker-universe selection behavior."""

import unittest
from unittest.mock import patch

from src.api_client import APIClientError
from src.universes import MARKET_UNIVERSES, get_ticker_options


class TestTickerUniverses(unittest.TestCase):
    """Verify the curated market universes exposed by the dashboard."""

    def test_expected_market_universes_are_available(self):
        self.assertEqual(set(MARKET_UNIVERSES), {"NIFTY 500", "Fortune 500"})
        self.assertTrue(MARKET_UNIVERSES["NIFTY 500"])
        self.assertTrue(MARKET_UNIVERSES["Fortune 500"])

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


if __name__ == "__main__":
    unittest.main()
