"""Versioned REST API for the internal normalized market-data store."""

from datetime import date
import os
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Query

from src.market_data.storage import MarketDataStore


app = FastAPI(
    title="StockPulse Market Data API",
    version="1.0.0",
    description="Private normalized end-of-day market-data service.",
)
store = MarketDataStore()


def require_service_token(x_market_data_token: Optional[str] = Header(default=None)) -> None:
    expected = os.getenv("MARKET_DATA_API_TOKEN")
    if expected and x_market_data_token != expected:
        raise HTTPException(status_code=401, detail="invalid market-data service token")


def serialize(row: Any) -> Dict[str, Any]:
    result = {}
    for key in row.__table__.columns.keys():
        value = getattr(row, key)
        result[key] = value.isoformat() if hasattr(value, "isoformat") else value
    return result


@app.on_event("startup")
def initialize_store() -> None:
    store.create_schema()


@app.get("/v1/health")
def health() -> dict:
    return {"status": "ok", "service": "market-data", "database": os.getenv("DATABASE_URL", "sqlite")}


@app.get("/v1/markets", dependencies=[Depends(require_service_token)])
def markets() -> dict:
    return {"markets": ["India", "United States", "Europe"]}


@app.get("/v1/exchanges", dependencies=[Depends(require_service_token)])
def exchanges() -> dict:
    return {"exchanges": [
        {"code": "NSE", "market": "India", "country": "India", "currency": "INR"},
        {"code": "BSE", "market": "India", "country": "India", "currency": "INR"},
        {"code": "NYSE", "market": "United States", "country": "United States", "currency": "USD"},
        {"code": "NASDAQ", "market": "United States", "country": "United States", "currency": "USD"},
        {"code": "LSE", "market": "Europe", "country": "United Kingdom", "currency": "GBP"},
        {"code": "XETRA", "market": "Europe", "country": "Germany", "currency": "EUR"},
    ]}


@app.get("/v1/instruments/search", dependencies=[Depends(require_service_token)])
def search_instruments(q: str = Query(min_length=1), exchange: Optional[str] = None, limit: int = 100) -> dict:
    return {"instruments": [serialize(row) for row in store.list_instruments(exchange, q, limit)]}


@app.get("/v1/exchanges/{exchange}/listings", dependencies=[Depends(require_service_token)])
def listings(exchange: str, limit: int = 500, offset: int = 0) -> dict:
    rows = store.list_instruments(exchange.upper(), limit=min(limit + offset, 500))
    return {"exchange": exchange.upper(), "offset": offset, "limit": limit, "listings": [serialize(row) for row in rows[offset:offset + limit]]}


@app.get("/v1/instruments/{instrument_id}/prices", dependencies=[Depends(require_service_token)])
def prices(instrument_id: str, start: Optional[date] = None, end: Optional[date] = None, limit: int = 1500) -> dict:
    return {"instrument_id": instrument_id, "prices": [serialize(row) for row in store.prices(instrument_id, start, end, limit)]}


@app.get("/v1/instruments/{instrument_id}", dependencies=[Depends(require_service_token)])
def instrument(instrument_id: str) -> dict:
    rows = store.list_instruments(limit=500)
    for row in rows:
        if row.instrument_id == instrument_id:
            return serialize(row)
    raise HTTPException(status_code=404, detail="instrument not found")


@app.get("/v1/instruments/{instrument_id}/fundamentals", dependencies=[Depends(require_service_token)])
def fundamentals(instrument_id: str) -> dict:
    # FinancialMetric storage/API is intentionally versioned separately from
    # the initial listing and OHLCV slice; no fabricated values are returned.
    return {"instrument_id": instrument_id, "metrics": [], "status": "not_ingested"}


@app.get("/v1/instruments/{instrument_id}/corporate-actions", dependencies=[Depends(require_service_token)])
def corporate_actions(instrument_id: str) -> dict:
    return {"instrument_id": instrument_id, "actions": [], "status": "not_ingested"}


@app.get("/v1/ingestion/runs", dependencies=[Depends(require_service_token)])
def ingestion_runs(limit: int = 50) -> dict:
    return {"runs": [serialize(row) for row in store.runs(limit)]}
