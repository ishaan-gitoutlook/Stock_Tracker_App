"""Curated stock universes and market listings used by the dashboard."""

from typing import Dict, List, Tuple


MARKET_UNIVERSES: Dict[str, Tuple[str, ...]] = {
    "NIFTY 500": (
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS",
        "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS",
        "LT.NS", "AXISBANK.NS", "MARUTI.NS", "SUNPHARMA.NS", "TATAMOTORS.NS",
        "TITAN.NS", "ASIANPAINT.NS", "WIPRO.NS", "NTPC.NS", "POWERGRID.NS",
        "BAJFINANCE.NS", "NESTLEIND.NS", "ULTRACEMCO.NS", "ONGC.NS", "ADANIENT.NS",
    ),
    "Fortune 500": (
        "WMT", "AMZN", "AAPL", "UNH", "CVS", "XOM", "JPM", "COST", "CVX",
        "MSFT", "GOOG", "GE", "HD", "MCK", "CAT", "META", "BAC", "NFLX",
        "PFE", "DIS",
    ),
    "NASDAQ 100": (
        "NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "AVGO",
        "COST", "ASML", "AMD", "ADBE", "NFLX", "CSCO", "QCOM", "INTC",
        "TXN", "AMAT", "MU", "PANW",
    ),
    "BSE Sensex 30": (
        "RELIANCE.BO", "TCS.BO", "HDFCBANK.BO", "ICICIBANK.BO", "INFY.BO",
        "HINDUNILVR.BO", "ITC.BO", "SBIN.BO", "BHARTIARTL.BO", "KOTAKBANK.BO",
        "LT.BO", "AXISBANK.BO", "MARUTI.BO", "SUNPHARMA.BO", "TATAMOTORS.BO",
        "TITAN.BO", "ASIANPAINT.BO", "WIPRO.BO", "NTPC.BO", "POWERGRID.BO",
    ),
    "FTSE 100 (UK)": (
        "AZN.L", "SHEL.L", "HSBA.L", "ULVR.L", "BP.L", "GSK.L", "RIO.L",
        "BATS.L", "REL.L", "DGE.L", "LSEG.L", "VOD.L", "LLOY.L", "BARC.L",
    ),
    "DAX 40 (Germany)": (
        "SAP.DE", "SIE.DE", "ALV.DE", "DTE.DE", "AIR.DE", "MBG.DE", "BMW.DE",
        "BAS.DE", "BAYN.DE", "MUV2.DE", "VOW3.DE", "DB1.DE",
    ),
    "Global Megacaps": (
        "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSM", "TCS.NS",
        "RELIANCE.NS", "SAP.DE", "ASML", "SHEL.L", "BABA",
    ),
}

# Display labels formatted cleanly to avoid Regional Indicator letter doubling on Windows
LISTING_DISPLAY_LABELS: Dict[str, str] = {
    "NIFTY 500": "🇮🇳 NIFTY 500 (India NSE)",
    "Fortune 500": "🇺🇸 S&P 500 / Fortune 500 (US)",
    "NASDAQ 100": "⚡ NASDAQ 100 (US Tech)",
    "BSE Sensex 30": "🏛️ BSE Sensex 30 (India BSE)",
    "FTSE 100 (UK)": "🇬🇧 FTSE 100 (UK London)",
    "DAX 40 (Germany)": "🇩🇪 DAX 40 (Germany XETRA)",
    "Global Megacaps": "🌐 Global Megacaps",
    "My Watchlist": "⭐ My Custom Watchlist",
}

# Complete bidirectional mapping with backwards compatibility for all label variants
LABEL_TO_UNIVERSE: Dict[str, str] = {
    **{v: k for k, v in LISTING_DISPLAY_LABELS.items()},
    "🇮🇳 NIFTY 500 (India NSE)": "NIFTY 500",
    "🇮🇳 India NIFTY 500 (NSE)": "NIFTY 500",
    "NIFTY 500": "NIFTY 500",
    "🇺🇸 S&P 500 / Fortune 500 (US)": "Fortune 500",
    "🇺🇸 US Fortune 500 / S&P 500": "Fortune 500",
    "Fortune 500": "Fortune 500",
    "⚡ NASDAQ 100 (US Tech)": "NASDAQ 100",
    "⚡ US NASDAQ 100 Tech": "NASDAQ 100",
    "NASDAQ 100": "NASDAQ 100",
    "🏛️ BSE Sensex 30 (India BSE)": "BSE Sensex 30",
    "🏛️ India BSE Sensex 30": "BSE Sensex 30",
    "BSE Sensex 30": "BSE Sensex 30",
    "🇬🇧 FTSE 100 (UK London)": "FTSE 100 (UK)",
    "🇬🇧 UK FTSE 100 (London LSE)": "FTSE 100 (UK)",
    "FTSE 100 (UK)": "FTSE 100 (UK)",
    "🇩🇪 DAX 40 (Germany XETRA)": "DAX 40 (Germany)",
    "🇩🇪 Germany DAX 40 (XETRA)": "DAX 40 (Germany)",
    "DAX 40 (Germany)": "DAX 40 (Germany)",
    "🌐 Global Megacaps": "Global Megacaps",
    "Global Megacaps": "Global Megacaps",
    "⭐ My Custom Watchlist": "My Watchlist",
    "⭐ Custom Watchlist": "My Watchlist",
    "My Watchlist": "My Watchlist",
}


def get_ticker_options(selected_universe: str, available_symbols: List[str]) -> List[str]:
    """Return ordered, de-duplicated ticker options for a selected universe or label."""
    actual_universe = LABEL_TO_UNIVERSE.get(selected_universe, selected_universe)
    if actual_universe == "My Watchlist" or actual_universe not in MARKET_UNIVERSES:
        return available_symbols

    return list(dict.fromkeys([
        *MARKET_UNIVERSES[actual_universe],
        *available_symbols,
    ]))
