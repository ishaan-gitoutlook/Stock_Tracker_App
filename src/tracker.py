"""Stock tracking core module for fetching financial quotes from Yahoo Finance."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import json
import logging
import time
from typing import Dict, Iterable, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)

DEFAULT_SYMBOLS = ("AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META")
REFRESH_SECONDS = 5
REQUEST_TIMEOUT_SECONDS = 8
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


@dataclass(frozen=True)
class StockQuote:
    """Represents a snapshot of a financial stock quote."""

    symbol: str
    name: str
    price: float
    currency: str
    previous_close: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    day_high: Optional[float] = None
    day_low: Optional[float] = None
    volume: Optional[int] = None

    @classmethod
    def from_meta(cls, symbol: str, meta: dict) -> "StockQuote":
        """Factory method to parse a StockQuote from Yahoo Finance meta response."""
        price = meta.get("regularMarketPrice")
        if price is None:
            raise ValueError(f"No regularMarketPrice in metadata for symbol '{symbol}'")

        prev_close = meta.get("chartPreviousClose") or meta.get("previousClose")
        change = None
        change_pct = None

        if prev_close and prev_close > 0:
            change = round(price - prev_close, 2)
            change_pct = round((change / prev_close) * 100, 2)

        name = meta.get("shortName") or meta.get("longName") or symbol

        return cls(
            symbol=symbol.upper(),
            name=name,
            price=round(float(price), 2),
            currency=meta.get("currency", "USD"),
            previous_close=round(float(prev_close), 2) if prev_close else None,
            change=change,
            change_percent=change_pct,
            day_high=meta.get("regularMarketDayHigh"),
            day_low=meta.get("regularMarketDayLow"),
            volume=meta.get("regularMarketVolume"),
        )


def fetch_single_quote(
    symbol: str, timeout: float = REQUEST_TIMEOUT_SECONDS
) -> Optional[StockQuote]:
    """Fetch the latest quote for an individual ticker symbol.

    Returns:
        StockQuote if successful, None if an error occurred.
    """
    clean_symbol = symbol.strip().upper()
    if not clean_symbol:
        return None

    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/"
        f"{quote(clean_symbol)}?range=1d&interval=1m"
    )
    request = Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.load(response)

        results = payload.get("chart", {}).get("result")
        if not results:
            logger.warning("No chart result found for symbol '%s'", clean_symbol)
            return None

        meta = results[0].get("meta", {})
        return StockQuote.from_meta(clean_symbol, meta)

    except (HTTPError, URLError, TimeoutError, KeyError, ValueError) as err:
        logger.warning("Failed to fetch quote for '%s': %s", clean_symbol, err)
        return None


def get_prices(
    symbols: Iterable[str] = DEFAULT_SYMBOLS,
    max_workers: int = 5,
) -> Dict[str, StockQuote]:
    """Fetch prices concurrently for multiple symbols using a thread pool.

    Args:
        symbols: Iterable of stock tickers (e.g. ['AAPL', 'MSFT']).
        max_workers: Maximum parallel worker threads.

    Returns:
        Dictionary mapping upper-cased symbol to StockQuote.
    """
    symbols_list = [s.strip().upper() for s in symbols if s.strip()]
    if not symbols_list:
        return {}

    quotes: Dict[str, StockQuote] = {}
    with ThreadPoolExecutor(max_workers=min(len(symbols_list), max_workers)) as executor:
        future_to_symbol = {
            executor.submit(fetch_single_quote, sym): sym for sym in symbols_list
        }
        for future in as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            try:
                quote_obj = future.result()
                if quote_obj:
                    quotes[symbol] = quote_obj
            except Exception as err:
                logger.error("Unexpected error fetching '%s': %s", symbol, err)

    # Maintain original order of requested symbols where available
    return {sym: quotes[sym] for sym in symbols_list if sym in quotes}


def stock_tracker(symbols: Iterable[str] = DEFAULT_SYMBOLS) -> None:
    """Run interactive terminal price ticker."""
    print("Starting Terminal Stock Tracker. Press Ctrl+C to exit...\n")
    while True:
        quotes = get_prices(symbols)
        # Clear screen ANSI escape codes
        print("\033[2J\033[H", end="")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"📈 Live Stock Tracker ({timestamp}) · Refreshing every {REFRESH_SECONDS}s")
        print("-" * 65)
        print(f"{'SYMBOL':<8} {'COMPANY':<22} {'PRICE':<12} {'CHANGE':<14}")
        print("-" * 65)

        for sym, q in quotes.items():
            chg_str = "N/A"
            if q.change is not None and q.change_percent is not None:
                sign = "+" if q.change >= 0 else ""
                chg_str = f"{sign}{q.change:.2f} ({sign}{q.change_percent:.2f}%)"

            price_str = f"{q.currency} {q.price:.2f}"
            print(f"{sym:<8} {q.name[:20]:<22} {price_str:<12} {chg_str:<14}")

        print("-" * 65)
        time.sleep(REFRESH_SECONDS)


if __name__ == "__main__":
    try:
        stock_tracker()
    except KeyboardInterrupt:
        print("\nStock tracker stopped.")
