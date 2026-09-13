"""Streamlit web dashboard for real-time stock price tracking."""

import time
from typing import Dict, List, Tuple
import streamlit as st

from src.tracker import (
    DEFAULT_SYMBOLS,
    REFRESH_SECONDS,
    StockQuote,
    get_prices,
)


@st.cache_data(ttl=REFRESH_SECONDS - 1, show_spinner=False)
def load_prices(symbols: Tuple[str, ...]) -> Dict[str, StockQuote]:
    """Fetch quotes with short TTL cache to avoid duplicate API spam."""
    return get_prices(symbols)


def render_dashboard() -> None:
    """Render the main view of metrics and market overview."""
    st.title("📈 Stock Tracker App")
    st.caption("Live financial market quotes powered by Yahoo Finance.")

    # Initialize custom symbols in session state
    if "available_symbols" not in st.session_state:
        st.session_state.available_symbols = list(DEFAULT_SYMBOLS)

    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Custom Ticker Adder
        with st.form("add_ticker_form", clear_on_submit=True):
            new_ticker = st.text_input(
                "Add Ticker Symbol",
                placeholder="e.g. NFLX, BABA, SPY",
            ).strip().upper()
            add_button = st.form_submit_button("Add Symbol")

            if add_button and new_ticker:
                if new_ticker not in st.session_state.available_symbols:
                    st.session_state.available_symbols.append(new_ticker)
                    st.success(f"Added {new_ticker}!")
                else:
                    st.info(f"{new_ticker} is already in the list.")

        selected_symbols: List[str] = st.multiselect(
            "Tracked Stocks",
            options=st.session_state.available_symbols,
            default=st.session_state.available_symbols[:4],
        )

        st.divider()
        st.markdown(
            "💡 **Tip**: Type any valid ticker symbol into the input box above to track it live."
        )

    if not selected_symbols:
        st.info("👈 Please select or add at least one stock from the sidebar.")
        return

    # Fetch live quotes
    quotes = load_prices(tuple(selected_symbols))

    if not quotes:
        st.warning("No price data could be retrieved. Please check your connection or symbol names.")
        return

    # Check for any symbols that failed
    missing_symbols = set(selected_symbols) - set(quotes.keys())
    if missing_symbols:
        st.warning(f"Could not retrieve data for: {', '.join(sorted(missing_symbols))}")

    # Top Metric Cards
    cols = st.columns(min(len(quotes), 4))
    for idx, (sym, quote_data) in enumerate(quotes.items()):
        col = cols[idx % 4]
        with col:
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

    # Market Overview Table
    st.subheader("📊 Market Overview")
    table_data = []
    for sym, q in quotes.items():
        day_range = "N/A"
        if q.day_low is not None and q.day_high is not None:
            day_range = f"{q.day_low:.2f} - {q.day_high:.2f}"

        table_data.append(
            {
                "Symbol": sym,
                "Company": q.name,
                "Price": f"{q.currency} {q.price:.2f}",
                "Change": f"{q.change:+.2f}" if q.change is not None else "N/A",
                "Change (%)": f"{q.change_percent:+.2f}%" if q.change_percent is not None else "N/A",
                "Day Range": day_range,
                "Volume": f"{q.volume:,}" if q.volume else "N/A",
            }
        )

    st.dataframe(table_data, hide_index=True, use_container_width=True)

    timestamp = time.strftime("%H:%M:%S")
    st.caption(f"Last updated: {timestamp} · Auto-refreshing every {REFRESH_SECONDS}s")


@st.fragment(run_every=f"{REFRESH_SECONDS}s")
def live_dashboard() -> None:
    """Fragment for periodic auto-refresh without full page reload."""
    render_dashboard()


def render_dashboard_app() -> None:
    """Main application runner."""
    st.set_page_config(
        page_title="Stock Tracker App",
        page_icon="📈",
        layout="wide",
    )
    live_dashboard()


if __name__ == "__main__":
    render_dashboard_app()
