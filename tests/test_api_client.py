"""Tests for the Streamlit-to-FastAPI HTTP client."""

import unittest
from unittest.mock import MagicMock, patch

from src.api_client import APIClientError, fetch_quotes


class TestAPIClient(unittest.TestCase):
    """Verify API response parsing and error handling without network calls."""

    @patch("src.api_client.urlopen")
    def test_fetch_quotes_parses_api_response(self, mock_urlopen):
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b'''{
            "quotes": [
                {
                    "symbol": "AAPL",
                    "name": "Apple Inc.",
                    "price": 200.5,
                    "currency": "USD",
                    "previous_close": 195.0,
                    "change": 5.5,
                    "change_percent": 2.82
                }
            ]
        }'''
        response.json.return_value = {
            "quotes": [
                {
                    "symbol": "AAPL",
                    "name": "Apple Inc.",
                    "price": 200.5,
                    "currency": "USD",
                    "previous_close": 195.0,
                    "change": 5.5,
                    "change_percent": 2.82,
                }
            ]
        }
        mock_urlopen.return_value = response

        quotes = fetch_quotes(["aapl"], base_url="http://api.test", fresh=True)

        self.assertEqual(quotes["AAPL"].price, 200.5)
        request = mock_urlopen.call_args.args[0]
        self.assertIn("symbols=AAPL", request.full_url)
        self.assertIn("fresh=true", request.full_url)

    @patch("src.api_client.urlopen", side_effect=OSError("connection refused"))
    def test_fetch_quotes_wraps_connection_errors(self, _mock_urlopen):
        with self.assertRaises(APIClientError):
            fetch_quotes(["AAPL"], base_url="http://api.test")

    @patch("src.api_client.urlopen")
    def test_fetch_quotes_skips_empty_symbol_list(self, mock_urlopen):
        self.assertEqual(fetch_quotes([]), {})
        mock_urlopen.assert_not_called()


if __name__ == "__main__":
    unittest.main()
