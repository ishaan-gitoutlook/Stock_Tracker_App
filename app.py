import time


def stock_tracker():
    stocks = {
        "AAPL": {"price": 175.45, "symbol": "AAPL"},
        "MSFT": {"price": 320.89, "symbol": "MSFT"},
        "GOOG": {"price": 135.67, "symbol": "GOOG"}
    }

    while True:
        for symbol in stocks:
            print(f"{stocks[symbol]['symbol']}: ${stocks[symbol]['price']:.2f}")
        time.sleep(5)  # Refresh every 5 seconds


if __name__ == "__main__":
    stock_tracker()
