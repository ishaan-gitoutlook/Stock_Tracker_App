"""Command-line entrypoint for scheduled market-data jobs."""

import argparse
import os

from src.market_data.ingest import IngestionService
from src.market_data.sources import EODHDSource
from src.market_data.storage import MarketDataStore
from src.research import EODHDProvider


def main() -> None:
    parser = argparse.ArgumentParser(description="Run StockPulse market-data ingestion")
    parser.add_argument("job", choices=["listings", "prices"])
    parser.add_argument("exchange")
    parser.add_argument("symbol", nargs="?")
    args = parser.parse_args()
    store = MarketDataStore()
    store.create_schema()
    service = IngestionService(store, EODHDSource(EODHDProvider()))
    if args.job == "listings":
        result = service.sync_listings(args.exchange)
    else:
        if not args.symbol:
            parser.error("symbol is required for prices job")
        result = service.ingest_prices(args.exchange, args.symbol)
    print(result)


if __name__ == "__main__":
    main()
