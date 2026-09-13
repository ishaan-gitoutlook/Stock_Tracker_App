"""Small standard-library HTTP client used by the Streamlit frontend."""

import json
import os
from typing import Dict, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from src.tracker import StockQuote


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
