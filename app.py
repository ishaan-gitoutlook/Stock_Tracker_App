"""Compatibility entry point for the command-line stock tracker."""

from src.app import stock_tracker


if __name__ == "__main__":
    try:
        stock_tracker()
    except KeyboardInterrupt:
        print("\nStock tracker stopped.")
