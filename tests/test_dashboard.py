"""Tests for dashboard ticker-universe selection behavior."""

import unittest

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


if __name__ == "__main__":
    unittest.main()
