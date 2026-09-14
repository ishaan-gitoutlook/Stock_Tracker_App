"""Stable identifiers and validation rules for source records."""

from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Iterable, Optional
import hashlib

from src.market_data.models import DailyPrice, Instrument


def stable_instrument_id(exchange: str, symbol: str, instrument_type: str = "Common Stock") -> str:
    key = f"{exchange.strip().upper()}|{symbol.strip().upper()}|{instrument_type.strip().upper()}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:32]


def normalize_instrument(row: Dict[str, Any], provider: str) -> Instrument:
    exchange = str(row.get("Exchange") or row.get("exchange") or row.get("exchange_code") or "").upper()
    symbol = str(row.get("Code") or row.get("code") or row.get("symbol") or "").upper().strip()
    name = str(row.get("Name") or row.get("name") or symbol).strip()
    instrument_type = str(row.get("Type") or row.get("type") or "Common Stock")
    if not exchange or not symbol:
        raise ValueError("instrument requires exchange and symbol")
    return Instrument(
        instrument_id=stable_instrument_id(exchange, symbol, instrument_type),
        symbol=symbol,
        name=name,
        exchange_code=exchange,
        instrument_type=instrument_type,
        isin=row.get("Isin") or row.get("isin"),
        figi=row.get("Figi") or row.get("figi"),
        country=row.get("Country") or row.get("country"),
        currency=row.get("Currency") or row.get("currency"),
        active=bool(row.get("IsActive", row.get("active", True))),
        source_provider=provider,
    )


def _decimal(value: Any) -> Optional[Decimal]:
    if value in (None, ""):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"invalid numeric value: {value!r}")


def normalize_daily_price(row: Dict[str, Any], instrument: Instrument, provider: str, run_id: str) -> DailyPrice:
    market_date = row.get("date") or row.get("market_date")
    if isinstance(market_date, datetime):
        market_date = market_date.date()
    elif isinstance(market_date, str):
        market_date = date.fromisoformat(market_date[:10])
    if not isinstance(market_date, date):
        raise ValueError("daily price requires an ISO market date")
    values = {key: _decimal(row.get(key)) for key in ("open", "high", "low", "close", "adjusted_close")}
    if any(value is not None and value < 0 for value in values.values()):
        raise ValueError("prices cannot be negative")
    volume = row.get("volume")
    if volume is not None and int(volume) < 0:
        raise ValueError("volume cannot be negative")
    return DailyPrice(
        instrument_id=instrument.instrument_id,
        market_date=market_date,
        **values,
        volume=int(volume) if volume is not None else None,
        currency=instrument.currency,
        source_provider=provider,
        source_timestamp=datetime.now(timezone.utc),
        ingestion_run_id=run_id,
    )
