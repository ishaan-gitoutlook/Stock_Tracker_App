"""Curated stock universes used by the dashboard."""

from typing import Dict, List, Tuple


MARKET_UNIVERSES: Dict[str, Tuple[str, ...]] = {
    "NIFTY 500": (
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS",
        "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS",
        "LT.NS", "AXISBANK.NS", "MARUTI.NS", "SUNPHARMA.NS", "TATAMOTORS.NS",
        "TITAN.NS", "ASIANPAINT.NS", "WIPRO.NS", "NTPC.NS", "POWERGRID.NS",
    ),
    "Fortune 500": (
        "WMT", "AMZN", "AAPL", "UNH", "CVS", "XOM", "JPM", "COST", "CVX",
        "MSFT", "GOOG", "GE", "HD", "MCK", "CAT", "META", "BAC", "NFLX",
        "PFE", "DIS",
    ),
}


def get_ticker_options(selected_universe: str, available_symbols: List[str]) -> List[str]:
    """Return ordered, de-duplicated ticker options for a selected universe."""
    if selected_universe == "My Watchlist":
        return available_symbols

    return list(dict.fromkeys([
        *MARKET_UNIVERSES[selected_universe],
        *available_symbols,
    ]))
