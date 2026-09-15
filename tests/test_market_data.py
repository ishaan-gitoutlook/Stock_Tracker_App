"""Fixture tests for custom market-data identifiers and validation."""

from datetime import date
from pathlib import Path
import sys
import unittest

# Ensure repository root is on sys.path when executed directly as a script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.market_data.normalization import normalize_daily_price, normalize_instrument, stable_instrument_id


class TestMarketDataNormalization(unittest.TestCase):
    def test_identifier_is_stable_and_exchange_scoped(self):
        self.assertEqual(stable_instrument_id("nse", "reliance"), stable_instrument_id("NSE", "RELIANCE"))
        self.assertNotEqual(stable_instrument_id("NSE", "RELIANCE"), stable_instrument_id("BSE", "RELIANCE"))

    def test_listing_normalization(self):
        instrument = normalize_instrument(
            {"Code": "RELIANCE", "Name": "Reliance Industries", "Exchange": "NSE", "Currency": "INR", "Isin": "INE002A01018"},
            "fixture",
        )
        self.assertEqual(instrument.symbol, "RELIANCE")
        self.assertEqual(instrument.exchange_code, "NSE")
        self.assertEqual(instrument.currency, "INR")

    def test_price_normalization_and_negative_value_rejection(self):
        instrument = normalize_instrument({"Code": "AAPL", "Name": "Apple", "Exchange": "NASDAQ", "Currency": "USD"}, "fixture")
        price = normalize_daily_price({"date": "2025-01-02", "open": "100", "close": "101", "volume": 10}, instrument, "fixture", "run-1")
        self.assertEqual(price.market_date, date(2025, 1, 2))
        self.assertEqual(price.instrument_id, instrument.instrument_id)
        with self.assertRaises(ValueError):
            normalize_daily_price({"date": "2025-01-02", "close": -1}, instrument, "fixture", "run-1")


if __name__ == "__main__":
    unittest.main()
