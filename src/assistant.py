"""AI Financial Assistant module supporting free cloud LLMs (Gemini), local Ollama, and offline financial heuristics."""

import json
import logging
import os
from typing import Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from src.tracker import StockQuote

logger = logging.getLogger(__name__)

DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_OLLAMA_MODEL = "llama3.2:3b"
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"
MAX_OUTPUT_TOKENS = 10_000
OUT_OF_SCOPE_REPLY = "I don't know."
INVESTMENT_DISCLAIMER = (
    "Disclaimer: Comparing stocks does not guarantee future performance. "
    "Investing involves risk, so make decisions at your own discretion."
)

STOCK_SCOPE_TERMS = (
    "stock", "stocks", "share", "shares", "ticker", "symbol", "price", "quote",
    "market", "performance", "gainer", "gainers", "loser", "losers", "gain",
    "loss", "volume", "trading", "portfolio", "watchlist", "nifty", "fortune",
    "invest", "investment", "buy", "sell", "dividend",
)
INVESTMENT_QUESTION_TERMS = (
    "better", "best", "buy", "sell", "invest", "investment", "recommend",
    "suggest", "worth", "choose", "pick", "should i",
)


def is_stock_question(question: str, quotes: Dict[str, StockQuote]) -> bool:
    """Return whether a question is related to tracked stocks or performance."""
    normalized = question.lower()
    if any(term in normalized for term in STOCK_SCOPE_TERMS):
        return True
    return any(
        symbol.lower() in normalized or quote.name.lower() in normalized
        for symbol, quote in quotes.items()
    )


def needs_investment_disclaimer(question: str) -> bool:
    """Identify questions that compare stocks or ask for investment direction."""
    normalized = question.lower()
    return any(term in normalized for term in INVESTMENT_QUESTION_TERMS)


def apply_response_guardrails(question: str, response: str) -> str:
    """Add the required risk disclaimer to investment-oriented responses."""
    if needs_investment_disclaimer(question) and INVESTMENT_DISCLAIMER not in response:
        return f"{response.rstrip()}\n\n{INVESTMENT_DISCLAIMER}"
    return response


def build_market_context(quotes: Dict[str, StockQuote]) -> str:
    """Build a concise, structured market snapshot from current stock quotes."""
    if not quotes:
        return "No active stock quotes currently selected in the dashboard."

    lines = ["Current Live Market Snapshot:"]
    for sym, q in quotes.items():
        chg_str = f"{q.change:+.2f} ({q.change_percent:+.2f}%)" if q.change is not None and q.change_percent is not None else "N/A"
        day_range = f"{q.day_low:.2f} - {q.day_high:.2f}" if q.day_low is not None and q.day_high is not None else "N/A"
        vol = f"{q.volume:,}" if q.volume else "N/A"
        lines.append(
            f"- {sym} ({q.name}): Price={q.currency} {q.price:.2f}, Daily Change={chg_str}, Day Range={day_range}, Volume={vol}"
        )
    return "\n".join(lines)


def build_system_prompt(quotes: Dict[str, StockQuote]) -> str:
    """Create system instructions with live market context and financial guardrails."""
    context = build_market_context(quotes)
    return (
        "You are an educational financial market assistant for the Stock Tracker App.\n"
        "Your role is to answer questions about tracked stocks and their performance using the provided live data.\n"
        "IMPORTANT RULES:\n"
        "1. Answer ONLY questions about stocks, tracked entities, market prices, or their performance.\n"
        "2. For anything outside that scope, reply exactly: I don't know.\n"
        "3. Ground all price and performance statements strictly in the provided Live Market Snapshot.\n"
        "4. Do NOT act as an all-knowing assistant or invent facts.\n"
        "5. Do NOT provide personalized investment advice or buy/sell recommendations. Never tell the user to buy, sell, or invest in a stock.\n"
        "6. If comparing which stock is better, explain the comparison neutrally and include a risk disclaimer.\n"
        "7. Always keep your response concise, educational, and professional.\n\n"
        f"{context}\n"
    )


class GeminiProvider:
    """Free Cloud LLM provider using Google Gemini API (Free Tier from Google AI Studio)."""

    def __init__(self, api_key: str, model: str = DEFAULT_GEMINI_MODEL):
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str, system_instruction: str, timeout: float = 12.0) -> Optional[str]:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
            f"?key={self.api_key}"
        )
        full_content = f"{system_instruction}\n\nUser Question: {prompt}\nAssistant:"
        payload = {
            "contents": [{"parts": [{"text": full_content}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": MAX_OUTPUT_TOKENS},
        }

        try:
            req = Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(req, timeout=timeout) as resp:
                data = json.load(resp)

            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts and "text" in parts[0]:
                    return parts[0]["text"].strip()
        except (HTTPError, URLError, TimeoutError, OSError, KeyError, ValueError) as err:
            logger.warning("Gemini API call failed: %s", err)
        return None


class OllamaProvider:
    """Free Local LLM provider calling a local Ollama instance (100% offline)."""

    def __init__(self, base_url: str = DEFAULT_OLLAMA_URL, model: str = DEFAULT_OLLAMA_MODEL):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def is_available(self, timeout: float = 1.5) -> bool:
        """Quick check to see if local Ollama daemon is running."""
        try:
            req = Request(f"{self.base_url}/api/tags", headers={"Accept": "application/json"})
            with urlopen(req, timeout=timeout) as resp:
                return resp.status == 200
        except Exception:
            return False

    def generate(self, prompt: str, system_instruction: str, timeout: float = 20.0) -> Optional[str]:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_instruction,
            "stream": False,
            "options": {"num_predict": MAX_OUTPUT_TOKENS, "temperature": 0.3},
        }

        try:
            req = Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(req, timeout=timeout) as resp:
                data = json.load(resp)
            reply = data.get("response")
            if reply:
                return reply.strip()
        except (HTTPError, URLError, TimeoutError, OSError, KeyError, ValueError) as err:
            logger.warning("Ollama API call failed: %s", err)
        return None


class HeuristicFinancialAnalyst:
    """Smart offline rule-based financial analyst requiring zero API keys, GPU, or internet."""

    @staticmethod
    def answer(question: str, quotes: Dict[str, StockQuote]) -> str:
        q_lower = question.lower()

        if not quotes:
            return (
                "No stocks are currently selected on the dashboard. "
                "Please select one or more stocks from the sidebar to analyze live prices."
            )

        quotes_list = list(quotes.values())

        # Top Gainer query
        if any(term in q_lower for term in ["top gainer", "largest increase", "best", "gain", "highest increase", "up the most"]):
            valid_gains = [q for q in quotes_list if q.change_percent is not None]
            if valid_gains:
                best = max(valid_gains, key=lambda q: q.change_percent or -9999)
                sign = "+" if (best.change or 0) >= 0 else ""
                return (
                    f"📈 **Top Performer:** **{best.name} ({best.symbol})** experienced the strongest movement among your tracked stocks, "
                    f"trading at **{best.currency} {best.price:.2f}** with a daily change of **{sign}{best.change:.2f} ({sign}{best.change_percent:.2f}%)**.\n\n"
                    f"*Note: For educational purposes only. Not financial advice.*"
                )

        # Top Loser query
        if any(term in q_lower for term in ["worst", "loser", "down the most", "largest drop", "fall", "decline"]):
            valid_losses = [q for q in quotes_list if q.change_percent is not None]
            if valid_losses:
                worst = min(valid_losses, key=lambda q: q.change_percent or 9999)
                sign = "+" if (worst.change or 0) >= 0 else ""
                return (
                    f"📉 **Biggest Decline:** **{worst.name} ({worst.symbol})** saw the weakest relative performance today, "
                    f"currently at **{worst.currency} {worst.price:.2f}** with a daily change of **{sign}{worst.change:.2f} ({sign}{worst.change_percent:.2f}%)**.\n\n"
                    f"*Note: For educational purposes only. Not financial advice.*"
                )

        # Highest price query
        if any(term in q_lower for term in ["highest price", "most expensive", "highest value"]):
            highest = max(quotes_list, key=lambda q: q.price)
            return (
                f"🏷️ **Highest Price:** **{highest.name} ({highest.symbol})** has the highest nominal share price among your tracked stocks at **{highest.currency} {highest.price:.2f}**."
            )

        # Lowest price query
        if any(term in q_lower for term in ["lowest price", "cheapest", "least expensive"]):
            lowest = min(quotes_list, key=lambda q: q.price)
            return (
                f"🏷️ **Lowest Price:** **{lowest.name} ({lowest.symbol})** is currently trading at the lowest nominal price in your selection at **{lowest.currency} {lowest.price:.2f}**."
            )

        # Volume query
        if "volume" in q_lower:
            valid_vol = [q for q in quotes_list if q.volume]
            if valid_vol:
                top_vol = max(valid_vol, key=lambda q: q.volume or 0)
                return (
                    f"📊 **Trading Volume:** **{top_vol.name} ({top_vol.symbol})** recorded the highest trading volume among your tracked entities "
                    f"with **{top_vol.volume:,} shares traded today**."
                )

        # General Summary / Compare / Default
        summary_lines = [
            f"Here is a summary of your currently tracked portfolio ({len(quotes)} stocks):"
        ]
        for q in quotes_list:
            chg = f"{q.change:+.2f} ({q.change_percent:+.2f}%)" if q.change is not None and q.change_percent is not None else "N/A"
            summary_lines.append(f"• **{q.symbol}** ({q.name}): {q.currency} {q.price:.2f} [{chg}]")

        summary_lines.append(
            "\n💡 *Tip: You can ask specific questions like 'Which stock gained the most?', 'Compare prices', or 'Which has the highest volume?'*"
        )
        return "\n".join(summary_lines)


def get_configured_gemini_key() -> Optional[str]:
    """Retrieve Gemini API key from environment variable or Streamlit secrets."""
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key

    try:
        import streamlit as st
        return st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None


def ask_assistant(
    question: str,
    quotes: Dict[str, StockQuote],
    ollama_base_url: Optional[str] = None,
    ollama_model: Optional[str] = None,
) -> Tuple[str, str]:
    """Ask the AI financial assistant with multi-tier provider resolution.

    Order of evaluation:
    1. Google Gemini API (if GEMINI_API_KEY is configured).
    2. Local Ollama (if Ollama daemon is active at http://127.0.0.1:11434).
    3. Built-in Heuristic Financial Analyst (offline zero-dependency fallback).

    Returns:
        Tuple of (response_markdown_text, provider_label_name)
    """
    clean_question = question.strip()
    if not clean_question:
        return OUT_OF_SCOPE_REPLY, "Scope Guard"

    if not is_stock_question(clean_question, quotes):
        return OUT_OF_SCOPE_REPLY, "Scope Guard"

    system_instruction = build_system_prompt(quotes)

    # 1. Try Gemini Free Cloud API
    gemini_key = get_configured_gemini_key()
    if gemini_key:
        provider = GeminiProvider(api_key=gemini_key)
        response = provider.generate(clean_question, system_instruction)
        if response:
            return apply_response_guardrails(clean_question, response), "Gemini Flash (Free Cloud)"

    # 2. Try Local Ollama Instance
    ollama_url = ollama_base_url or os.getenv("OLLAMA_BASE_URL", DEFAULT_OLLAMA_URL)
    model = ollama_model or os.getenv("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
    ollama = OllamaProvider(base_url=ollama_url, model=model)

    if ollama.is_available():
        response = ollama.generate(clean_question, system_instruction)
        if response:
            return apply_response_guardrails(clean_question, response), f"Ollama ({model})"

    # 3. Fallback to Heuristic Financial Analyst
    heuristic_reply = HeuristicFinancialAnalyst.answer(clean_question, quotes)
    return apply_response_guardrails(clean_question, heuristic_reply), "Built-in Financial Analyst"
