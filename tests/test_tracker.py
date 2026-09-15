"""Unit tests for the stock tracker core logic."""

from pathlib import Path
import sys
import unittest
from unittest.mock import MagicMock, patch

# Ensure repository root is on sys.path when executed directly as a script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.tracker import StockQuote, fetch_single_quote, get_prices


class TestStockTracker(unittest.TestCase):
    """Test suite for stock tracker calculations and parsing."""

    def test_stock_quote_from_meta_success(self):
        """Test parsing valid Yahoo Finance metadata into a StockQuote."""
        meta = {
            "regularMarketPrice": 150.0,
            "chartPreviousClose": 140.0,
            "currency": "USD",
            "shortName": "Test Company",
            "regularMarketDayHigh": 155.0,
            "regularMarketDayLow": 139.0,
            "regularMarketVolume": 1200000,
        }

        quote = StockQuote.from_meta("TEST", meta)

        self.assertEqual(quote.symbol, "TEST")
        self.assertEqual(quote.name, "Test Company")
        self.assertEqual(quote.price, 150.0)
        self.assertEqual(quote.currency, "USD")
        self.assertEqual(quote.previous_close, 140.0)
        self.assertEqual(quote.change, 10.0)
        self.assertEqual(quote.change_percent, 7.14)
        self.assertEqual(quote.day_high, 155.0)
        self.assertEqual(quote.day_low, 139.0)
        self.assertEqual(quote.volume, 1200000)

    def test_stock_quote_from_meta_missing_price(self):
        """Test that missing regularMarketPrice raises ValueError."""
        meta = {"currency": "USD"}
        with self.assertRaises(ValueError):
            StockQuote.from_meta("TEST", meta)

    def test_stock_quote_fallback_name(self):
        """Test that name falls back to symbol when not provided in meta."""
        meta = {"regularMarketPrice": 100.0}
        quote = StockQuote.from_meta("XYZ", meta)
        self.assertEqual(quote.name, "XYZ")

    def test_fetch_single_quote_empty_symbol(self):
        """Test that empty or whitespace symbol returns None without calling API."""
        self.assertIsNone(fetch_single_quote(""))
        self.assertIsNone(fetch_single_quote("   "))

    def test_get_prices_empty_list(self):
        """Test that empty symbol list returns empty dictionary."""
        self.assertEqual(get_prices([]), {})

    @patch("src.tracker.urlopen")
    def test_fetch_single_quote_mocked_network(self, mock_urlopen):
        """Test network call parsing with mocked response."""
        mock_response = MagicMock()
        mock_response.read.return_value = b"""
        {
            "chart": {
                "result": [
                    {
                        "meta": {
                            "regularMarketPrice": 200.5,
                            "chartPreviousClose": 195.0,
                            "currency": "USD",
                            "shortName": "Mock Corp"
                        }
                    }
                ]
            }
        }
        """
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        quote = fetch_single_quote("MCK")
        self.assertIsNotNone(quote)
        self.assertEqual(quote.symbol, "MCK")
        self.assertEqual(quote.price, 200.5)
        self.assertEqual(quote.change, 5.5)
        self.assertEqual(quote.name, "Mock Corp")


if __name__ == "__main__":
    unittest.main()
