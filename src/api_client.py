"""Small standard-library HTTP client used by the Streamlit frontend."""

import json
import os
from typing import Dict, Iterable, List, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from src.tracker import StockQuote
from src.research import Instrument


DEFAULT_API_URL = "http://127.0.0.1:8000"


class APIClientError(RuntimeError):
    """Raised when the FastAPI backend cannot return quote data."""


def configured_api_url(base_url: str | None = None) -> str:
    """Resolve the API URL from an argument, environment, or Streamlit secret."""
    if base_url:
        return base_url.rstrip("/")

    api_url = os.getenv("STOCK_API_URL", DEFAULT_API_URL)
    try:
        import streamlit as st

        api_url = st.secrets.get("STOCK_API_URL", api_url)
    except (ImportError, RuntimeError, FileNotFoundError):
        # The client is also used by unit tests and non-Streamlit processes.
        pass
    return str(api_url).rstrip("/")


def configured_market_data_url(base_url: str | None = None) -> str | None:
    """Resolve the private normalized market-data API URL."""
    if base_url:
        return base_url.rstrip("/")
    value = os.getenv("MARKET_DATA_API_URL")
    try:
        import streamlit as st
        value = st.secrets.get("MARKET_DATA_API_URL", value)
    except (ImportError, RuntimeError, FileNotFoundError):
        pass
    return str(value).rstrip("/") if value else None


def fetch_market_listings(exchange: str, base_url: str | None = None, limit: int = 500) -> List[Instrument]:
    """Fetch normalized listings from the private market-data service."""
    api_url = configured_market_data_url(base_url)
    if not api_url:
        raise APIClientError("MARKET_DATA_API_URL is not configured")
    token = os.getenv("MARKET_DATA_API_TOKEN")
    try:
        import streamlit as st
        token = st.secrets.get("MARKET_DATA_API_TOKEN", token)
    except (ImportError, RuntimeError, FileNotFoundError):
        pass
    request = Request(
        f"{api_url}/v1/exchanges/{quote(exchange.upper())}/listings?limit={min(limit, 500)}",
        headers={"Accept": "application/json", "X-Market-Data-Token": str(token or "")},
    )
    try:
        with urlopen(request, timeout=15) as response:
            payload = json.load(response)
        return [Instrument.from_payload(item) for item in payload.get("listings", [])]
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, TypeError) as err:
        raise APIClientError(f"Could not reach market-data API at {api_url}: {err}") from err


def search_market_instruments(query: str, exchange: str | None = None, base_url: str | None = None, limit: int = 100) -> List[Instrument]:
    """Search normalized instruments without exposing source-provider credentials."""
    api_url = configured_market_data_url(base_url)
    if not api_url:
        raise APIClientError("MARKET_DATA_API_URL is not configured")
    token = os.getenv("MARKET_DATA_API_TOKEN")
    try:
        import streamlit as st
        token = st.secrets.get("MARKET_DATA_API_TOKEN", token)
    except (ImportError, RuntimeError, FileNotFoundError):
        pass
    params = f"q={quote(query)}&limit={min(limit, 500)}"
    if exchange:
        params += f"&exchange={quote(exchange.upper())}"
    request = Request(f"{api_url}/v1/instruments/search?{params}", headers={"Accept": "application/json", "X-Market-Data-Token": str(token or "")})
    try:
        with urlopen(request, timeout=15) as response:
            payload = json.load(response)
        return [Instrument.from_payload(item) for item in payload.get("instruments", [])]
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, TypeError) as err:
        raise APIClientError(f"Could not search market-data API at {api_url}: {err}") from err


def fetch_quotes(
    symbols: Iterable[str],
    base_url: str | None = None,
    fresh: bool = False,
    timeout: float = 10,
) -> Dict[str, StockQuote]:
    """Fetch quote data from the FastAPI backend."""
    normalized = [symbol.strip().upper() for symbol in symbols if symbol.strip()]
    if not normalized:
        return {}

    api_url = configured_api_url(base_url)
    query = quote(",".join(normalized), safe=",")
    url = f"{api_url}/api/v1/quotes?symbols={query}&fresh={'true' if fresh else 'false'}"
    request = Request(url, headers={"Accept": "application/json"})

    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as err:
        raise APIClientError(f"Could not reach stock API at {api_url}: {err}") from err

    try:
        return {
            item["symbol"]: StockQuote(**item)
            for item in payload.get("quotes", [])
        }
    except (AttributeError, KeyError, TypeError, ValueError) as err:
        raise APIClientError("Stock API returned an invalid quote response") from err


def send_chat_message(
    message: str,
    symbols: Iterable[str],
    base_url: str | None = None,
    ollama_model: str | None = None,
    timeout: float = 25.0,
) -> Tuple[str, str]:
    """Send a question to the FastAPI chat assistant endpoint.

    Returns:
        Tuple of (reply_text, provider_name).
    Raises:
        APIClientError if the API cannot be reached or returns an error.
    """
    normalized = [symbol.strip().upper() for symbol in symbols if symbol.strip()]
    api_url = configured_api_url(base_url)
    url = f"{api_url}/api/v1/chat"

    payload = {
        "message": message,
        "symbols": normalized,
        "ollama_model": ollama_model,
    }
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            data = json.load(response)
        return str(data["reply"]), str(data["provider"])
    except (HTTPError, URLError, TimeoutError, OSError, KeyError, ValueError) as err:
        raise APIClientError(f"Could not reach stock API at {api_url}: {err}") from err
