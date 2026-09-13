import json
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


SYMBOLS = ("AAPL", "MSFT", "GOOG")
REFRESH_SECONDS = 5


def get_prices(symbols=SYMBOLS):
    """Return the latest available prices for Yahoo Finance symbols."""
    prices = {}
    for symbol in symbols:
        url = (
            "https://query1.finance.yahoo.com/v8/finance/chart/"
            f"{quote(symbol)}?range=1d&interval=1m"
        )
        request = Request(url, headers={"User-Agent": "StockTracker/1.0"})
        with urlopen(request, timeout=10) as response:
            payload = json.load(response)

        metadata = payload["chart"]["result"][0]["meta"]
        price = metadata.get("regularMarketPrice")
        if price is None:
            raise ValueError(f"No current price returned for {symbol}")
        prices[symbol] = (price, metadata.get("currency", ""))
    return prices


def stock_tracker():
    while True:
        try:
            prices = get_prices()
            print("\033[2J\033[H", end="")
            print(f"Live stock prices (refreshing every {REFRESH_SECONDS}s)\n")
            for symbol, (price, currency) in prices.items():
                print(f"{symbol}: {currency} {price:.2f}")
        except (HTTPError, URLError, TimeoutError, KeyError, ValueError) as error:
            print(f"Unable to retrieve prices: {error}")
        time.sleep(REFRESH_SECONDS)


if __name__ == "__main__":
    try:
        stock_tracker()
    except KeyboardInterrupt:
        print("\nStock tracker stopped.")
