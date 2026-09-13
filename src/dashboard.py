"""Streamlit web dashboard with live quotes and free AI financial assistant."""

import time
from typing import Dict, List, Tuple
import streamlit as st

from src.api_client import APIClientError, fetch_quotes, send_chat_message
from src.assistant import ask_assistant
from src.tracker import DEFAULT_SYMBOLS, REFRESH_SECONDS, StockQuote, get_prices
from src.universes import MARKET_UNIVERSES, get_ticker_options


@st.cache_data(ttl=REFRESH_SECONDS - 1, show_spinner=False)
def load_prices(symbols: Tuple[str, ...]) -> Tuple[Dict[str, StockQuote], str]:
    """Fetch quotes through the FastAPI backend with graceful fallback to direct fetching."""
    try:
        return fetch_quotes(symbols), "FastAPI"
    except APIClientError:
        return get_prices(symbols), "Direct"


def query_assistant(prompt: str, symbols: List[str], quotes: Dict[str, StockQuote]) -> Tuple[str, str]:
    """Query assistant via FastAPI if available, falling back to direct in-process assistant."""
    try:
        return send_chat_message(prompt, symbols, timeout=15.0)
    except APIClientError:
        return ask_assistant(prompt, quotes)


def render_sidebar() -> List[str]:
    """Render sidebar filters, universe selection, and custom ticker form."""
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
            "Tracked Stocks / Entities",
            options=ticker_options,
            default=ticker_options[:4],
        )

        st.divider()
        if st.button("↻ Refresh Quotes Now", use_container_width=True):
            load_prices.clear()
            st.rerun()

        st.markdown("💡 **Tip**: Choose a universe, select entities, or add custom symbols.")

    st.session_state.current_selected_symbols = selected_symbols
    return selected_symbols


@st.fragment(run_every=f"{REFRESH_SECONDS}s")
def render_live_market(selected_symbols: List[str]) -> None:
    """Live updating fragment for market metrics and overview table."""
    st.title("📈 Stock Tracker App")
    st.caption("Live financial market quotes powered by Yahoo Finance & FastAPI.")

    if not selected_symbols:
        st.info("👈 Please select or add at least one stock from the sidebar.")
        return

    try:
        quotes, source = load_prices(tuple(selected_symbols))
    except Exception as err:
        st.error(f"Unable to retrieve stock data: {err}")
        return

    st.session_state.cached_quotes = quotes

    if not quotes:
        st.warning("No price data could be retrieved. Please check your connection or symbol names.")
        return

    missing_symbols = set(selected_symbols) - set(quotes.keys())
    if missing_symbols:
        st.warning(f"Could not retrieve data for: {', '.join(sorted(missing_symbols))}")

    # Metric Cards
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
    st.caption(f"Last updated: {timestamp} · Auto-refreshing every {REFRESH_SECONDS}s · Source: {source}")


def render_ai_assistant(selected_symbols: List[str]) -> None:
    """Render the AI Financial Assistant chat interface."""
    st.divider()
    st.subheader("🤖 AI Financial Assistant")
    st.caption("Ask questions about market movements, compare tracked stocks, or explore financial concepts.")

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "Hello! I am your AI Financial Assistant. Ask me anything about your tracked stocks, top gainers, or market trends!",
                "provider": "Assistant",
            }
        ]

    # Quick prompt buttons
    st.markdown("**Quick Prompts:**")
    prompt_cols = st.columns(4)
    quick_prompt = None

    with prompt_cols[0]:
        if st.button("📈 Top Gainer Today?", use_container_width=True):
            quick_prompt = "Which tracked stock had the largest increase today?"
    with prompt_cols[1]:
        if st.button("📉 Biggest Decline?", use_container_width=True):
            quick_prompt = "Which stock had the largest drop today?"
    with prompt_cols[2]:
        if st.button("📊 Portfolio Summary", use_container_width=True):
            quick_prompt = "Summarize the performance of all my currently selected stocks."
    with prompt_cols[3]:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_messages = [
                {
                    "role": "assistant",
                    "content": "Chat history cleared. How can I help you today?",
                    "provider": "Assistant",
                }
            ]
            st.rerun()

    # Display conversation history
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("provider") and msg["role"] == "assistant" and msg["provider"] != "Assistant":
                st.caption(f"⚡ *Engine: {msg['provider']}*")

    # Handle user query (from chat input or quick prompt button)
    user_input = st.chat_input("Ask about your tracked stocks, comparisons, or financial metrics...")
    prompt_to_send = user_input or quick_prompt

    if prompt_to_send:
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt_to_send})
        with st.chat_message("user"):
            st.markdown(prompt_to_send)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing market data..."):
                quotes = st.session_state.get("cached_quotes", {})
                reply, provider = query_assistant(prompt_to_send, selected_symbols, quotes)
                st.markdown(reply)
                st.caption(f"⚡ *Engine: {provider}*")

        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": reply,
            "provider": provider,
        })
        if quick_prompt:
            st.rerun()


def render_dashboard_app() -> None:
    """Main application runner."""
    st.set_page_config(page_title="Stock Tracker App", page_icon="📈", layout="wide")
    selected_symbols = render_sidebar()
    render_live_market(selected_symbols)
    render_ai_assistant(selected_symbols)


if __name__ == "__main__":
    render_dashboard_app()
