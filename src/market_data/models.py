"""Provider-independent market-data domain models."""

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Exchange:
    code: str
    name: str
    market: str
    country: str
    currency: str
    timezone: str
    source_provider: str = ""


@dataclass(frozen=True)
class Instrument:
    instrument_id: str
    symbol: str
    name: str
    exchange_code: str
    instrument_type: str = "Common Stock"
    isin: Optional[str] = None
    figi: Optional[str] = None
    country: Optional[str] = None
    currency: Optional[str] = None
    active: bool = True
    source_provider: str = ""


@dataclass(frozen=True)
class DailyPrice:
    instrument_id: str
    market_date: date
    open: Optional[Decimal] = None
    high: Optional[Decimal] = None
    low: Optional[Decimal] = None
    close: Optional[Decimal] = None
    adjusted_close: Optional[Decimal] = None
    volume: Optional[int] = None
    currency: Optional[str] = None
    adjustment_status: str = "unadjusted"
    source_provider: str = ""
    source_timestamp: Optional[datetime] = None
    ingestion_run_id: Optional[str] = None
    revision: int = 1
    availability: str = "available"


@dataclass(frozen=True)
class CorporateAction:
    instrument_id: str
    action_date: date
    action_type: str
    value: Optional[Decimal] = None
    ratio: Optional[str] = None
    currency: Optional[str] = None
    source_provider: str = ""
    ingestion_run_id: Optional[str] = None


@dataclass(frozen=True)
class FinancialMetric:
    instrument_id: str
    period_end: date
    period_type: str
    metric: str
    value: Optional[Decimal] = None
    currency: Optional[str] = None
    source_provider: str = ""
    ingestion_run_id: Optional[str] = None
    revision: int = 1


@dataclass(frozen=True)
class IngestionRun:
    run_id: str
    job_type: str
    exchange_code: Optional[str]
    status: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    records_seen: int = 0
    records_published: int = 0
    error_message: Optional[str] = None
    source_provider: str = ""
