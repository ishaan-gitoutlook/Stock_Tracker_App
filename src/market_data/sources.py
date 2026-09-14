"""Source contracts and development adapters for market-data ingestion."""

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Protocol

from src.research import EODHDProvider


class MarketDataSource(Protocol):
    name: str

    def listings(self, exchange: str) -> List[Dict[str, Any]]: ...

    def daily_prices(self, symbol: str, exchange: str, period: str = "5y") -> List[Dict[str, Any]]: ...


@dataclass
class EODHDSource:
    """Development adapter; replace with licensed exchange adapters in production."""

    provider: EODHDProvider
    name: str = "eodhd-development"

    def listings(self, exchange: str) -> List[Dict[str, Any]]:
        return [item.__dict__ for item in self.provider.exchange_symbols(exchange)]

    def daily_prices(self, symbol: str, exchange: str, period: str = "5y") -> List[Dict[str, Any]]:
        rows = self.provider.history(f"{symbol}.{exchange}", period)
        return [item.__dict__ for item in rows]


@dataclass
class FixtureSource:
    """Deterministic source for tests and local pipeline development."""

    listing_rows: Dict[str, List[Dict[str, Any]]]
    price_rows: Dict[str, List[Dict[str, Any]]]
    name: str = "fixture"

    def listings(self, exchange: str) -> List[Dict[str, Any]]:
        return list(self.listing_rows.get(exchange.upper(), []))

    def daily_prices(self, symbol: str, exchange: str, period: str = "5y") -> List[Dict[str, Any]]:
        return list(self.price_rows.get(f"{symbol.upper()}.{exchange.upper()}", []))
