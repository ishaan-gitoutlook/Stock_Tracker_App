"""SQL persistence for the custom market-data service.

SQLite is the local default; set DATABASE_URL to a PostgreSQL SQLAlchemy URL
for deployed environments (for example postgresql+psycopg://...).
"""

from datetime import date, datetime
import hashlib
import json
import os
from typing import Any, Iterable, List, Optional

from sqlalchemy import Boolean, Date, DateTime, Integer, Numeric, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from src.market_data.models import DailyPrice, Exchange, FinancialMetric, IngestionRun, Instrument


class Base(DeclarativeBase):
    pass


class ExchangeRow(Base):
    __tablename__ = "exchanges"
    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    market: Mapped[str] = mapped_column(String(64), index=True)
    country: Mapped[str] = mapped_column(String(64))
    currency: Mapped[str] = mapped_column(String(16))
    timezone: Mapped[str] = mapped_column(String(64))
    source_provider: Mapped[str] = mapped_column(String(64))


class InstrumentRow(Base):
    __tablename__ = "instruments"
    instrument_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    symbol: Mapped[str] = mapped_column(String(64), index=True)
    name: Mapped[str] = mapped_column(String(255))
    exchange_code: Mapped[str] = mapped_column(String(32), index=True)
    instrument_type: Mapped[str] = mapped_column(String(64))
    isin: Mapped[Optional[str]] = mapped_column(String(32), nullable=True, index=True)
    figi: Mapped[Optional[str]] = mapped_column(String(32), nullable=True, index=True)
    country: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    source_provider: Mapped[str] = mapped_column(String(64))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class DailyPriceRow(Base):
    __tablename__ = "daily_prices"
    instrument_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    market_date: Mapped[date] = mapped_column(Date, primary_key=True)
    revision: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    open: Mapped[Optional[float]] = mapped_column(Numeric(24, 8), nullable=True)
    high: Mapped[Optional[float]] = mapped_column(Numeric(24, 8), nullable=True)
    low: Mapped[Optional[float]] = mapped_column(Numeric(24, 8), nullable=True)
    close: Mapped[Optional[float]] = mapped_column(Numeric(24, 8), nullable=True)
    adjusted_close: Mapped[Optional[float]] = mapped_column(Numeric(24, 8), nullable=True)
    volume: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    adjustment_status: Mapped[str] = mapped_column(String(32), default="unadjusted")
    source_provider: Mapped[str] = mapped_column(String(64))
    source_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    ingestion_run_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    availability: Mapped[str] = mapped_column(String(32), default="available")


class TradingCalendarRow(Base):
    __tablename__ = "trading_calendars"
    exchange_code: Mapped[str] = mapped_column(String(32), primary_key=True)
    market_date: Mapped[date] = mapped_column(Date, primary_key=True)
    is_open: Mapped[bool] = mapped_column(Boolean, default=True)
    session_open: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    session_close: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    source_provider: Mapped[str] = mapped_column(String(64))


class CorporateActionRow(Base):
    __tablename__ = "corporate_actions"
    instrument_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    action_date: Mapped[date] = mapped_column(Date, primary_key=True)
    action_type: Mapped[str] = mapped_column(String(32), primary_key=True)
    revision: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    value: Mapped[Optional[float]] = mapped_column(Numeric(24, 8), nullable=True)
    ratio: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    source_provider: Mapped[str] = mapped_column(String(64))
    ingestion_run_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)


class CompanyProfileRow(Base):
    __tablename__ = "company_profiles"
    instrument_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    sector: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_provider: Mapped[str] = mapped_column(String(64))
    source_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ingestion_run_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)


class FinancialMetricRow(Base):
    __tablename__ = "financial_metrics"
    instrument_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    period_end: Mapped[date] = mapped_column(Date, primary_key=True)
    period_type: Mapped[str] = mapped_column(String(32), primary_key=True)
    metric: Mapped[str] = mapped_column(String(128), primary_key=True)
    revision: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    value: Mapped[Optional[float]] = mapped_column(Numeric(24, 8), nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    source_provider: Mapped[str] = mapped_column(String(64))
    ingestion_run_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)


class SourcePayloadRow(Base):
    __tablename__ = "source_payloads"
    payload_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source_provider: Mapped[str] = mapped_column(String(64))
    dataset: Mapped[str] = mapped_column(String(64))
    exchange_code: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    payload_json: Mapped[str] = mapped_column(Text)
    checksum: Mapped[str] = mapped_column(String(64), index=True)


class IngestionRunRow(Base):
    __tablename__ = "ingestion_runs"
    run_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    job_type: Mapped[str] = mapped_column(String(64))
    exchange_code: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    records_seen: Mapped[int] = mapped_column(Integer, default=0)
    records_published: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_provider: Mapped[str] = mapped_column(String(64))


class MarketDataStore:
    """Repository used by both workers and the versioned API."""

    def __init__(self, database_url: Optional[str] = None):
        url = database_url or os.getenv("DATABASE_URL", "sqlite:///./market_data.db")
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        self.engine = create_engine(url, future=True)
        self.sessions = sessionmaker(self.engine, expire_on_commit=False)

    def create_schema(self) -> None:
        Base.metadata.create_all(self.engine)

    def save_instruments(self, instruments: Iterable[Instrument]) -> int:
        count = 0
        with self.sessions.begin() as session:
            for item in instruments:
                row = session.get(InstrumentRow, item.instrument_id)
                values = item.__dict__.copy()
                values["updated_at"] = datetime.utcnow()
                if row is None:
                    session.add(InstrumentRow(**values))
                else:
                    for key, value in values.items(): setattr(row, key, value)
                count += 1
        return count

    def save_prices(self, prices: Iterable[DailyPrice]) -> int:
        count = 0
        with self.sessions.begin() as session:
            for item in prices:
                values = item.__dict__.copy()
                existing = session.get(DailyPriceRow, (item.instrument_id, item.market_date, item.revision))
                if existing is None: session.add(DailyPriceRow(**values))
                else:
                    for key, value in values.items(): setattr(existing, key, value)
                count += 1
        return count

    def save_raw_payload(self, dataset: str, exchange: str, payload: Any, provider: str) -> str:
        encoded = json.dumps(payload, default=str, sort_keys=True)
        checksum = hashlib.sha256(encoded.encode()).hexdigest()
        payload_id = hashlib.sha256(f"{dataset}|{exchange}|{checksum}".encode()).hexdigest()[:32]
        with self.sessions.begin() as session:
            if session.get(SourcePayloadRow, payload_id) is None:
                session.add(SourcePayloadRow(
                    payload_id=payload_id,
                    source_provider=provider,
                    dataset=dataset,
                    exchange_code=exchange,
                    captured_at=datetime.utcnow(),
                    payload_json=encoded,
                    checksum=checksum,
                ))
        return payload_id

    def list_instruments(self, exchange: Optional[str] = None, query: Optional[str] = None, limit: int = 100) -> List[InstrumentRow]:
        limit = min(max(limit, 1), 500)
        with self.sessions() as session:
            stmt = select(InstrumentRow).where(InstrumentRow.active.is_(True))
            if exchange: stmt = stmt.where(InstrumentRow.exchange_code == exchange.upper())
            if query:
                term = f"%{query.upper()}%"
                stmt = stmt.where((InstrumentRow.symbol.ilike(term)) | (InstrumentRow.name.ilike(term)))
            return list(session.scalars(stmt.order_by(InstrumentRow.symbol).limit(limit)))

    def prices(self, instrument_id: str, start: Optional[date], end: Optional[date], limit: int = 1500) -> List[DailyPriceRow]:
        with self.sessions() as session:
            stmt = select(DailyPriceRow).where(DailyPriceRow.instrument_id == instrument_id)
            if start: stmt = stmt.where(DailyPriceRow.market_date >= start)
            if end: stmt = stmt.where(DailyPriceRow.market_date <= end)
            return list(session.scalars(stmt.order_by(DailyPriceRow.market_date.desc()).limit(min(limit, 5000))))

    def runs(self, limit: int = 50) -> List[IngestionRunRow]:
        with self.sessions() as session:
            stmt = select(IngestionRunRow).order_by(IngestionRunRow.started_at.desc()).limit(min(limit, 200))
            return list(session.scalars(stmt))
