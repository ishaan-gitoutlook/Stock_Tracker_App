"""Provider-neutral global equity research data services.

The EODHD adapter is deliberately small and defensive: upstream payloads are
large and change over time, so unavailable fields are represented as ``None``.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import os
from typing import Any, Dict, Iterable, List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


MARKET_EXCHANGES = {
    "India": ("NSE", "BSE"),
    "United States": ("NYSE", "NASDAQ", "AMEX", "US"),
    "Europe": ("LSE", "XETRA", "EURONEXT", "SIX", "BME", "NASDAQ NORDIC"),
}


def market_for_exchange(exchange: str) -> Optional[str]:
    value = (exchange or "").upper().replace("-", " ")
    for market, exchanges in MARKET_EXCHANGES.items():
        if value in exchanges or any(item in value for item in exchanges if len(item) > 3):
            return market
    return None


def _first(data: Dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if data.get(key) is not None:
            return data[key]
    return None


@dataclass(frozen=True)
class Instrument:
    symbol: str
    name: str
    exchange: str = ""
    country: str = ""
    currency: str = ""
    type: str = "Common Stock"

    @classmethod
    def from_payload(cls, value: Dict[str, Any]) -> "Instrument":
        exchange = str(_first(value, "Exchange", "exchange", "exchange_name") or "")
        return cls(
            symbol=str(_first(value, "Code", "code", "symbol") or "").upper(),
            name=str(_first(value, "Name", "name", "description") or "Unknown instrument"),
            exchange=exchange,
            country=str(_first(value, "Country", "country") or ""),
            currency=str(_first(value, "Currency", "currency") or ""),
            type=str(_first(value, "Type", "type") or "Common Stock"),
        )


@dataclass(frozen=True)
class HistoryPoint:
    date: str
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    adjusted_close: Optional[float] = None
    volume: Optional[int] = None


@dataclass(frozen=True)
class ResearchProfile:
    symbol: str
    name: str
    exchange: str = ""
    currency: str = ""
    country: str = ""
    quote: Dict[str, Any] = field(default_factory=dict)
    valuation: Dict[str, Any] = field(default_factory=dict)
    profitability: Dict[str, Any] = field(default_factory=dict)
    statements: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    dividends: List[Dict[str, Any]] = field(default_factory=list)
    company: Dict[str, Any] = field(default_factory=dict)
    source: str = "EODHD"
    as_of: Optional[str] = None


class ResearchProviderError(RuntimeError):
    """Raised when the configured market-data provider cannot answer."""


class EODHDProvider:
    """Minimal EODHD REST adapter. API key is read from EODHD_API_KEY."""

    def __init__(self, api_key: Optional[str] = None, timeout: float = 12.0):
        self.api_key = api_key or os.getenv("EODHD_API_KEY")
        self.timeout = timeout
        self.base_url = os.getenv("EODHD_BASE_URL", "https://eodhd.com/api").rstrip("/")

    def _get(self, path: str, **params: Any) -> Any:
        if not self.api_key:
            raise ResearchProviderError("EODHD_API_KEY is not configured")
        params["api_token"] = self.api_key
        query = "&".join(f"{quote(str(k))}={quote(str(v))}" for k, v in params.items() if v is not None)
        request = Request(f"{self.base_url}/{path.lstrip('/')}?{query}", headers={"Accept": "application/json"})
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.load(response)
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as err:
            raise ResearchProviderError(f"EODHD request failed: {err}") from err

    def exchanges(self) -> List[Dict[str, Any]]:
        return self._get("exchanges-list/")

    def search(self, query: str, market: Optional[str] = None, exchange: Optional[str] = None) -> List[Instrument]:
        rows = self._get("search/", query=query) or []
        results = [Instrument.from_payload(row) for row in rows if isinstance(row, dict)]
        if market:
            results = [item for item in results if market_for_exchange(item.exchange) == market or item.country in market_countries(market)]
        if exchange:
            results = [item for item in results if exchange.upper() in item.exchange.upper()]
        return results

    def quote(self, symbol: str) -> Dict[str, Any]:
        return self._get(f"real-time/{quote(symbol)}")

    def history(self, symbol: str, period: str = "1y") -> List[HistoryPoint]:
        rows = self._get(f"eod/{quote(symbol)}", period=period, fmt="json") or []
        return [HistoryPoint(date=str(row.get("date", "")), open=row.get("open"), high=row.get("high"), low=row.get("low"), close=row.get("close"), adjusted_close=row.get("adjusted_close"), volume=row.get("volume")) for row in rows if isinstance(row, dict)]

    def fundamentals(self, symbol: str) -> ResearchProfile:
        data = self._get(f"v1.1/fundamentals/{quote(symbol)}") or {}
        general = data.get("General", {})
        highlights = data.get("Highlights", {})
        valuation = data.get("Valuation", {})
        technicals = data.get("Technicals", {})
        financials = data.get("Financials", {})
        profile = ResearchProfile(
            symbol=str(general.get("Code", symbol)).upper(),
            name=str(general.get("Name", symbol)),
            exchange=str(general.get("Exchange", "")),
            currency=str(general.get("CurrencyCode", "")),
            country=str(general.get("CountryName", "")),
            valuation={**valuation},
            profitability={**highlights, **technicals},
            statements={key: value for key, value in financials.items() if isinstance(value, dict)},
            dividends=data.get("SplitsDividends", {}).get("Dividend", []) or [],
            company=general,
            as_of=datetime.now(timezone.utc).isoformat(),
        )
        try:
            profile = ResearchProfile(**{**profile.__dict__, "quote": self.quote(symbol)})
        except ResearchProviderError:
            pass
        return profile


def market_countries(market: str) -> set[str]:
    if market == "India":
        return {"India"}
    if market == "United States":
        return {"USA", "United States", "US"}
    return {"United Kingdom", "Germany", "France", "Netherlands", "Belgium", "Switzerland", "Spain", "Sweden", "Denmark", "Finland", "Norway", "Italy", "Portugal", "Ireland"}
