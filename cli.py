"""Command-line interface entry point for the stock tracker."""

from src.tracker import stock_tracker


if __name__ == "__main__":
    try:
        stock_tracker()
    except KeyboardInterrupt:
        print("\nStock tracker stopped.")
