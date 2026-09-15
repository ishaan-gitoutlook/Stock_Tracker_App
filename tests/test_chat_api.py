"""Unit tests for the FastAPI chat endpoint and api_client chat integration."""

import json
from pathlib import Path
import sys
import unittest
from unittest.mock import MagicMock, patch

# Ensure repository root is on sys.path when executed directly as a script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.api import app
from src.api_client import APIClientError, send_chat_message
from src.tracker import StockQuote


class TestChatAPI(unittest.TestCase):
    """Test the POST /api/v1/chat endpoint and client wrapper."""

    @patch("src.api.get_prices")
    @patch("src.assistant.ask_assistant")
    def test_chat_endpoint_returns_valid_payload(self, mock_ask, mock_get_prices):
        from src.api import ChatRequest, chat_assistant

        mock_get_prices.return_value = {
            "AAPL": StockQuote(symbol="AAPL", name="Apple Inc.", price=150.0, currency="USD")
        }
        mock_ask.return_value = ("Apple had steady gains.", "Mock Provider")

        res = chat_assistant(
            ChatRequest(message="How is AAPL doing?", symbols=["AAPL"])
        )

        self.assertEqual(res.reply, "Apple had steady gains.")
        self.assertEqual(res.provider, "Mock Provider")
        self.assertIn("AAPL", res.symbols_used)

    @patch("src.api_client.urlopen")
    def test_send_chat_message_parses_response(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.__enter__.return_value = mock_response
        mock_response.read.return_value = json.dumps({
            "reply": "Market looks bullish today.",
            "provider": "Gemini Free Tier",
            "symbols_used": ["NVDA"],
        }).encode("utf-8")
        mock_urlopen.return_value = mock_response

        reply, provider = send_chat_message("Summarize NVDA", ["NVDA"], base_url="http://mock-api")
        self.assertEqual(reply, "Market looks bullish today.")
        self.assertEqual(provider, "Gemini Free Tier")

    @patch("src.api_client.urlopen", side_effect=OSError("Network unreachable"))
    def test_send_chat_message_raises_client_error(self, _mock_urlopen):
        with self.assertRaises(APIClientError):
            send_chat_message("Summarize NVDA", ["NVDA"], base_url="http://mock-api")


if __name__ == "__main__":
    unittest.main()
