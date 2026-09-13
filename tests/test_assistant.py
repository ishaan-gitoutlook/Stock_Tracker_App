"""Unit tests for the AI Financial Assistant and provider integrations."""

import json
import unittest
from unittest.mock import MagicMock, patch

from src.assistant import (
    GeminiProvider,
    HeuristicFinancialAnalyst,
    OllamaProvider,
    ask_assistant,
    build_market_context,
    build_system_prompt,
)
from src.tracker import StockQuote


class TestAssistantContext(unittest.TestCase):
    """Test prompt and market context building."""

    def setUp(self):
        self.sample_quotes = {
            "AAPL": StockQuote(
                symbol="AAPL",
                name="Apple Inc.",
                price=150.0,
                currency="USD",
                previous_close=140.0,
                change=10.0,
                change_percent=7.14,
                day_high=155.0,
                day_low=139.0,
                volume=1500000,
            ),
            "MSFT": StockQuote(
                symbol="MSFT",
                name="Microsoft Corporation",
                price=300.0,
                currency="USD",
                previous_close=310.0,
                change=-10.0,
                change_percent=-3.23,
                day_high=315.0,
                day_low=298.0,
                volume=800000,
            ),
        }

    def test_build_market_context_includes_tickers(self):
        context = build_market_context(self.sample_quotes)
        self.assertIn("AAPL", context)
        self.assertIn("MSFT", context)
        self.assertIn("Apple Inc.", context)
        self.assertIn("150.00", context)
        self.assertIn("+10.00 (+7.14%)", context)

    def test_build_market_context_empty_quotes(self):
        context = build_market_context({})
        self.assertIn("No active stock quotes", context)

    def test_build_system_prompt_includes_guardrails(self):
        prompt = build_system_prompt(self.sample_quotes)
        self.assertIn("educational financial market assistant", prompt)
        self.assertIn("Do NOT provide personalized investment advice", prompt)
        self.assertIn("AAPL", prompt)


class TestHeuristicFinancialAnalyst(unittest.TestCase):
    """Test offline heuristic financial reasoning without external LLMs."""

    def setUp(self):
        self.sample_quotes = {
            "AAPL": StockQuote(
                symbol="AAPL",
                name="Apple Inc.",
                price=150.0,
                currency="USD",
                previous_close=140.0,
                change=10.0,
                change_percent=7.14,
                day_high=155.0,
                day_low=139.0,
                volume=1500000,
            ),
            "MSFT": StockQuote(
                symbol="MSFT",
                name="Microsoft Corp",
                price=300.0,
                currency="USD",
                previous_close=310.0,
                change=-10.0,
                change_percent=-3.23,
                day_high=315.0,
                day_low=298.0,
                volume=800000,
            ),
        }

    def test_top_gainer_query(self):
        reply = HeuristicFinancialAnalyst.answer("Which stock had the top gainer today?", self.sample_quotes)
        self.assertIn("Top Performer", reply)
        self.assertIn("AAPL", reply)
        self.assertIn("+7.14%", reply)

    def test_worst_decline_query(self):
        reply = HeuristicFinancialAnalyst.answer("Which stock had the largest drop?", self.sample_quotes)
        self.assertIn("Biggest Decline", reply)
        self.assertIn("MSFT", reply)
        self.assertIn("-3.23%", reply)

    def test_highest_price_query(self):
        reply = HeuristicFinancialAnalyst.answer("What is the highest price stock?", self.sample_quotes)
        self.assertIn("Highest Price", reply)
        self.assertIn("MSFT", reply)
        self.assertIn("300.00", reply)

    def test_volume_query(self):
        reply = HeuristicFinancialAnalyst.answer("Which stock has the highest volume?", self.sample_quotes)
        self.assertIn("Trading Volume", reply)
        self.assertIn("AAPL", reply)
        self.assertIn("1,500,000", reply)

    def test_general_summary_query(self):
        reply = HeuristicFinancialAnalyst.answer("Summarize my portfolio", self.sample_quotes)
        self.assertIn("AAPL", reply)
        self.assertIn("MSFT", reply)


class TestProviderIntegration(unittest.TestCase):
    """Test Gemini and Ollama providers with mocked HTTP responses."""

    @patch("src.assistant.urlopen")
    def test_gemini_provider_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.__enter__.return_value = mock_response
        mock_response.read.return_value = json.dumps({
            "candidates": [
                {"content": {"parts": [{"text": "Apple is outperforming today."}]}}
            ]
        }).encode("utf-8")
        mock_urlopen.return_value = mock_response

        provider = GeminiProvider(api_key="fake-key-123")
        res = provider.generate("How is Apple doing?", "system prompt")
        self.assertEqual(res, "Apple is outperforming today.")

    @patch("src.assistant.urlopen")
    def test_ollama_provider_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.__enter__.return_value = mock_response
        mock_response.read.return_value = json.dumps({
            "response": "Microsoft showed a slight pull-back."
        }).encode("utf-8")
        mock_urlopen.return_value = mock_response

        provider = OllamaProvider(base_url="http://mock-ollama:11434")
        res = provider.generate("How is Microsoft doing?", "system prompt")
        self.assertEqual(res, "Microsoft showed a slight pull-back.")

    @patch("src.assistant.get_configured_gemini_key", return_value=None)
    @patch("src.assistant.OllamaProvider.is_available", return_value=False)
    def test_ask_assistant_fallback_to_heuristic(self, _mock_ollama, _mock_gemini):
        # Without Gemini key or Ollama running, fallback to heuristic analyst
        quotes = {
            "TSLA": StockQuote(symbol="TSLA", name="Tesla Inc.", price=220.0, currency="USD", change=5.0, change_percent=2.33)
        }
        reply, provider_name = ask_assistant("Which stock is top gainer?", quotes)
        self.assertEqual(provider_name, "Built-in Financial Analyst")
        self.assertIn("TSLA", reply)


if __name__ == "__main__":
    unittest.main()
