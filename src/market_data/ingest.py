"""Idempotent ingestion orchestration with raw-payload retention."""

from datetime import datetime
import hashlib
import json
import logging
import os
from pathlib import Path
import time
from typing import Any, Dict, Iterable, List
from uuid import uuid4

from src.market_data.models import IngestionRun
from src.market_data.normalization import normalize_daily_price, normalize_instrument
from src.market_data.sources import MarketDataSource
from src.market_data.storage import IngestionRunRow, MarketDataStore, SourcePayloadRow

logger = logging.getLogger(__name__)


class IngestionService:
    def __init__(self, store: MarketDataStore, source: MarketDataSource, raw_dir: str | None = None, retries: int = 3):
        self.store = store
        self.source = source
        self.raw_dir = Path(raw_dir or os.getenv("MARKET_DATA_RAW_DIR", "./market_data_raw"))
        self.retries = max(1, retries)

    def _capture(self, dataset: str, exchange: str, payload: Any) -> None:
        encoded = json.dumps(payload, default=str, sort_keys=True)
        checksum = hashlib.sha256(encoded.encode()).hexdigest()
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        path = self.raw_dir / f"{datetime.utcnow():%Y%m%dT%H%M%S}_{exchange}_{dataset}_{checksum[:12]}.json"
        path.write_text(encoded, encoding="utf-8")
        self.store.save_raw_payload(dataset, exchange, payload, self.source.name)

    def _call(self, function, *args):
        last_error = None
        for attempt in range(self.retries):
            try:
                return function(*args)
            except Exception as err:  # source-specific errors must not crash the worker
                last_error = err
                if attempt + 1 < self.retries:
                    time.sleep(2 ** attempt)
        raise last_error  # type: ignore[misc]

    def sync_listings(self, exchange: str) -> IngestionRun:
        run_id = uuid4().hex
        started = datetime.utcnow()
        try:
            raw = self._call(self.source.listings, exchange)
            self._capture("listings", exchange, raw)
            instruments = [normalize_instrument(row, self.source.name) for row in raw]
            published = self.store.save_instruments(instruments)
            result = IngestionRun(run_id, "listings", exchange, "published", started, datetime.utcnow(), len(raw), published, source_provider=self.source.name)
        except Exception as err:
            logger.exception("Listing ingestion failed for %s", exchange)
            result = IngestionRun(run_id, "listings", exchange, "failed", started, datetime.utcnow(), error_message=str(err), source_provider=self.source.name)
        self._save_run(result)
        return result

    def ingest_prices(self, exchange: str, symbol: str) -> IngestionRun:
        run_id = uuid4().hex
        started = datetime.utcnow()
        try:
            raw = self._call(self.source.daily_prices, symbol, exchange, "5y")
            self._capture("daily_prices", exchange, raw)
            instrument_rows = self.store.list_instruments(exchange, symbol, limit=1)
            if not instrument_rows:
                raise ValueError(f"instrument {symbol}.{exchange} is not registered")
            instrument = normalize_instrument({"Code": instrument_rows[0].symbol, "Name": instrument_rows[0].name, "Exchange": exchange, "Currency": instrument_rows[0].currency, "Type": instrument_rows[0].instrument_type}, self.source.name)
            prices = [normalize_daily_price(row, instrument, self.source.name, run_id) for row in raw]
            published = self.store.save_prices(prices)
            result = IngestionRun(run_id, "daily_prices", exchange, "published", started, datetime.utcnow(), len(raw), published, source_provider=self.source.name)
        except Exception as err:
            logger.exception("Price ingestion failed for %s/%s", exchange, symbol)
            result = IngestionRun(run_id, "daily_prices", exchange, "failed", started, datetime.utcnow(), error_message=str(err), source_provider=self.source.name)
        self._save_run(result)
        return result

    def _save_run(self, run: IngestionRun) -> None:
        with self.store.sessions.begin() as session:
            session.add(IngestionRunRow(**run.__dict__))
