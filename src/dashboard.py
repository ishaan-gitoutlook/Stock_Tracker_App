"""Streamlit web dashboard for real-time stock price tracking."""

import time
from typing import Dict, List, Tuple

import streamlit as st

from src.api_client import APIClientError, fetch_quotes
from src.tracker import DEFAULT_SYMBOLS, REFRESH_SECONDS, StockQuote
from src.universes import MARKET_UNIVERSES, get_ticker_options


@st.cache_data(ttl=REFRESH_SECONDS - 1, show_spinner=False)
def load_prices(symbols: Tuple[str, ...]) -> Dict[str, StockQuote]:
    """Fetch quotes through the FastAPI backend with a short UI cache."""
    return fetch_quotes(symbols)


def render_dashboard() -> None:
    """Render the main view of metrics and market overview."""
    st.title("📈 Stock Tracker App")
    st.caption("Live financial market quotes powered by the FastAPI backend.")

    if "available_symbols" not in st.session_state:
        st.session_state.available_symbols = list(DEFAULT_SYMBOLS)

    with st.sidebar:
        st.header("⚙️ Configuration")

        with st.form("add_ticker_form", clear_on_submit=True):
            new_ticker = st.text_input("Add Ticker Symbol", placeholder="e.g. NFLX, BABA, SPY").strip().upper()
            add_button = st.form_submit_button("Add Symbol")
            if add_button and new_ticker:
                if new_ticker not in st.session_state.available_symbols:
                    st.session_state.available_symbols.append(new_ticker)
                    st.success(f"Added {new_ticker}!")
                else:
                    st.info(f"{new_ticker} is already in the list.")

        selected_universe = st.selectbox(
            "Ticker universe",
            ["My Watchlist", *MARKET_UNIVERSES],
            help="Browse curated NIFTY 500 or Fortune 500 entities, or use your watchlist.",
        )
        ticker_options = get_ticker_options(
            selected_universe, st.session_state.available_symbols
        )

        selected_symbols: List[str] = st.multiselect(
            "Tracked Stocks / Entities", options=ticker_options, default=ticker_options[:4]
        )

        st.divider()
        if st.button("↻ Refresh now", use_container_width=True):
            load_prices.clear()
            st.rerun()
        st.markdown("💡 **Tip**: Choose a universe, select its entities, or add any valid ticker symbol.")

    if not selected_symbols:
        st.info("👈 Please select or add at least one stock from the sidebar.")
        return

    try:
        quotes = load_prices(tuple(selected_symbols))
    except APIClientError as err:
        st.error(f"Stock API unavailable: {err}")
        st.info("Start the backend with: uvicorn src.api:app --reload")
        return
    if not quotes:
        st.warning("No price data could be retrieved. Please check your connection or symbol names.")
        return

    missing_symbols = set(selected_symbols) - set(quotes.keys())
    if missing_symbols:
        st.warning(f"Could not retrieve data for: {', '.join(sorted(missing_symbols))}")

    cols = st.columns(min(len(quotes), 4))
    for idx, (sym, quote_data) in enumerate(quotes.items()):
        with cols[idx % 4]:
            delta_str = None
            if quote_data.change is not None and quote_data.change_percent is not None:
                sign = "+" if quote_data.change >= 0 else ""
                delta_str = f"{sign}{quote_data.change:.2f} ({sign}{quote_data.change_percent:.2f}%)"
            st.metric(
                label=f"{sym} · {quote_data.name}",
                value=f"{quote_data.currency} {quote_data.price:.2f}",
                delta=delta_str,
            )

    st.divider()
    st.subheader("📊 Market Overview")
    table_data = []
    for sym, quote_data in quotes.items():
        day_range = "N/A"
        if quote_data.day_low is not None and quote_data.day_high is not None:
            day_range = f"{quote_data.day_low:.2f} - {quote_data.day_high:.2f}"
        table_data.append({
            "Symbol": sym,
            "Company": quote_data.name,
            "Price": f"{quote_data.currency} {quote_data.price:.2f}",
            "Change": f"{quote_data.change:+.2f}" if quote_data.change is not None else "N/A",
            "Change (%)": f"{quote_data.change_percent:+.2f}%" if quote_data.change_percent is not None else "N/A",
            "Day Range": day_range,
            "Volume": f"{quote_data.volume:,}" if quote_data.volume else "N/A",
        })
    st.dataframe(table_data, hide_index=True, use_container_width=True)
    timestamp = time.strftime("%H:%M:%S")
    st.caption(f"Last updated: {timestamp} · Auto-refreshing every {REFRESH_SECONDS}s")


@st.fragment(run_every=f"{REFRESH_SECONDS}s")
def live_dashboard() -> None:
    """Fragment for periodic auto-refresh without full page reloads."""
    render_dashboard()


def render_dashboard_app() -> None:
    """Main application runner."""
    st.set_page_config(page_title="Stock Tracker App", page_icon="📈", layout="wide")
    live_dashboard()


if __name__ == "__main__":
    render_dashboard_app()
