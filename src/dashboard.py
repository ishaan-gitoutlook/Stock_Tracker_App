"""Streamlit web dashboard with live quotes and a stock performance assistant."""

import time
from typing import Dict, List, Tuple

import streamlit as st

from src.api_client import APIClientError, fetch_quotes, send_chat_message
from src.assistant import ask_assistant
from src.themes import (
    DISPLAY_TO_NAME,
    NAME_TO_DISPLAY,
    THEME_ALIASES,
    THEME_DISPLAY_OPTIONS,
    THEMES,
    build_theme_css,
    resolve_theme,
)
from src.tracker import DEFAULT_SYMBOLS, REFRESH_SECONDS, StockQuote, get_prices
from src.universes import MARKET_UNIVERSES, get_ticker_options
from src.research_ui import render_research_dashboard


@st.cache_data(ttl=REFRESH_SECONDS - 1, show_spinner=False)
def load_prices(symbols: Tuple[str, ...]) -> Tuple[Dict[str, StockQuote], str]:
    """Fetch quotes through FastAPI, falling back to direct fetching."""
    try:
        return fetch_quotes(symbols), "FastAPI"
    except APIClientError:
        return get_prices(symbols), "Direct"


def query_assistant(prompt: str, symbols: List[str], quotes: Dict[str, StockQuote]) -> Tuple[str, str]:
    """Query FastAPI, falling back to the local assistant when unavailable."""
    try:
        return send_chat_message(prompt, symbols, timeout=15.0)
    except APIClientError:
        return ask_assistant(prompt, quotes)


def render_sidebar() -> List[str]:
    """Render sidebar filters, universe selection, and custom ticker form."""
    if "available_symbols" not in st.session_state:
        st.session_state.available_symbols = list(DEFAULT_SYMBOLS)

    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="brand-mark">SP</div>
                <div class="brand-info">
                    <div class="brand-name">StockPulse</div>
                    <div class="brand-caption">MARKET INTELLIGENCE</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Theme selection with multiple modern options
        current_theme_key = st.session_state.get("theme_mode", "Midnight Navy")
        if current_theme_key in THEME_ALIASES:
            current_theme_key = THEME_ALIASES[current_theme_key]
        if current_theme_key not in THEMES:
            current_theme_key = "Midnight Navy"

        current_display = NAME_TO_DISPLAY.get(
            current_theme_key, THEMES["Midnight Navy"].display_name
        )
        try:
            default_index = THEME_DISPLAY_OPTIONS.index(current_display)
        except ValueError:
            default_index = 0

        selected_display = st.selectbox(
            "Theme Palette",
            options=THEME_DISPLAY_OPTIONS,
            index=default_index,
            help="Choose from 7 modern dark and light aesthetics.",
            key="theme_palette_select",
        )
        st.session_state.theme_mode = DISPLAY_TO_NAME.get(
            selected_display, "Midnight Navy"
        )

        st.header("Configuration")
        with st.form("add_ticker_form", clear_on_submit=True):
            new_ticker = st.text_input(
                "Add Ticker Symbol", placeholder="e.g. NFLX, BABA, SPY"
            ).strip().upper()
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
            help="Browse NIFTY 500 or Fortune 500 entities, or use your watchlist.",
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
        if st.button("ðŸ”„ Refresh Quotes Now", use_container_width=True):
            load_prices.clear()
            st.rerun()
        st.caption("Choose a universe, select entities, or add custom symbols.")

    st.session_state.current_selected_symbols = selected_symbols
    return selected_symbols


@st.fragment(run_every=f"{REFRESH_SECONDS}s")
def render_live_market(selected_symbols: List[str]) -> None:
    """Render live market metrics and the overview table."""
    if not selected_symbols:
        st.markdown(
            f"""
            <div class="hero-panel">
                <div class="hero-copy">
                    <div class="eyebrow"><span class="live-dot"></span> LIVE MARKET INTELLIGENCE</div>
                    <h1>Market Pulse</h1>
                    <p>Track momentum, compare performance, and stay close to the market.</p>
                </div>
                <div class="hero-stats-row">
                    <div class="hero-stat-card">
                        <strong>0</strong>
                        <span>Tracked Entities</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.info("Please select or add at least one stock from the sidebar.")
        return

    try:
        quotes, source = load_prices(tuple(selected_symbols))
    except Exception as err:
        st.error(f"Unable to retrieve stock data: {err}")
        return

    st.session_state.cached_quotes = quotes

    # Calculate market sentiment stats
    gainers_count = sum(1 for q in quotes.values() if (q.change or 0) > 0)
    decliners_count = sum(1 for q in quotes.values() if (q.change or 0) < 0)

    st.markdown(
        f"""
        <div class="hero-panel">
            <div class="hero-copy">
                <div class="eyebrow"><span class="live-dot"></span> LIVE MARKET INTELLIGENCE</div>
                <h1>Market Pulse</h1>
                <p>Track momentum, compare performance, and stay close to the market.</p>
            </div>
            <div class="hero-stats-row">
                <div class="hero-stat-card">
                    <strong>{len(selected_symbols)}</strong>
                    <span>Tracked</span>
                </div>
                <div class="hero-stat-card">
                    <strong>{gainers_count}G Â· {decliners_count}D</strong>
                    <span>Breadth</span>
                </div>
                <div class="hero-stat-card">
                    <strong>{REFRESH_SECONDS}s</strong>
                    <span>Auto-Sync</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not quotes:
        st.warning("No price data could be retrieved. Check your connection or symbol names.")
        return

    missing_symbols = set(selected_symbols) - set(quotes.keys())
    if missing_symbols:
        st.warning(f"Could not retrieve data for: {', '.join(sorted(missing_symbols))}")

    st.markdown(
        """
        <div class="section-heading">
            <div class="section-kicker">LIVE SNAPSHOT</div>
            <div class="section-title">Tracked performance</div>
            <div class="section-subtitle">Real-time valuation and intraday movements</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(min(len(quotes), 4))
    for idx, (sym, quote_data) in enumerate(quotes.items()):
        with cols[idx % 4]:
            delta_str = None
            if quote_data.change is not None and quote_data.change_percent is not None:
                sign = "+" if quote_data.change >= 0 else ""
                delta_str = f"{sign}{quote_data.change:.2f} ({sign}{quote_data.change_percent:.2f}%)"
            st.metric(
                label=f"{sym} Â· {quote_data.name}",
                value=f"{quote_data.currency} {quote_data.price:.2f}",
                delta=delta_str,
            )

    st.markdown(
        """
        <div class="section-heading overview-heading">
            <div class="section-kicker">MARKET DATA</div>
            <div class="section-title">Market overview</div>
            <div class="section-subtitle">Intraday price movement, range, and trading liquidity</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    table_data = []
    for sym, quote_data in quotes.items():
        day_range = "N/A"
        if quote_data.day_low is not None and quote_data.day_high is not None:
            day_range = f"{quote_data.day_low:.2f} - {quote_data.day_high:.2f}"
        table_data.append(
            {
                "Symbol": sym,
                "Company": quote_data.name,
                "Price": f"{quote_data.currency} {quote_data.price:.2f}",
                "Change": f"{quote_data.change:+.2f}" if quote_data.change is not None else "N/A",
                "Change (%)": f"{quote_data.change_percent:+.2f}%" if quote_data.change_percent is not None else "N/A",
                "Day Range": day_range,
                "Volume": f"{quote_data.volume:,}" if quote_data.volume else "N/A",
            }
        )
    st.dataframe(table_data, hide_index=True, use_container_width=True)
    timestamp = time.strftime("%H:%M:%S")
    st.caption(f"Last updated: {timestamp} Â· Auto-refreshing every {REFRESH_SECONDS}s Â· Data feed: {source}")


def render_ai_assistant(selected_symbols: List[str]) -> None:
    """Render the optimized stock performance AI assistant inside the floating chat popover."""
    now_str = time.strftime("%I:%M %p")

    # Header with title, live status, and action buttons
    header_cols = st.columns([0.8, 0.2])
    with header_cols[0]:
        st.markdown(
            f"""
            <div class="chat-header">
                <div class="chat-header-left">
                    <div class="chat-avatar">âœ¨</div>
                    <div class="chat-title-group">
                        <div class="chat-title">StockPulse Copilot</div>
                        <div class="chat-status"><span class="chat-status-dot"></span> Live Market Grounding</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with header_cols[1]:
        if st.button("ðŸ§¹ Clear", help="Reset conversation history", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()

    # Active Watchlist Context Bar
    if selected_symbols:
        pills_html = "".join([f'<span class="context-ticker">{s}</span>' for s in selected_symbols[:8]])
        if len(selected_symbols) > 8:
            pills_html += f'<span class="context-ticker">+{len(selected_symbols) - 8} more</span>'
        st.markdown(
            f"""
            <div class="chat-context-bar">
                <span class="context-label">Active Context:</span>
                {pills_html}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="chat-context-bar">
                <span class="context-label">Active Context:</span>
                <span style="color: var(--ui-bearish); font-size: 0.72rem;">No symbols selected. Select stocks from the sidebar for live analysis.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Initialize chat history if absent
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": (
                    "**Hello! I am your StockPulse Copilot.**\n\n"
                    "Ask me about intraday performance, top gainers, price spreads, "
                    "or volume leaders for your tracked stocks."
                ),
                "provider": "StockPulse AI",
                "time": now_str,
            }
        ]

    # Quick Suggestion Action Chips
    chip_cols = st.columns(4)
    quick_prompt = None
    with chip_cols[0]:
        if st.button("ðŸš€ Top Gainer", help="Find the stock with largest gain", use_container_width=True):
            quick_prompt = "Which tracked stock had the largest increase today?"
    with chip_cols[1]:
        if st.button("ðŸ”» Biggest Drop", help="Find the stock with largest decline", use_container_width=True):
            quick_prompt = "Which stock had the largest drop today?"
    with chip_cols[2]:
        if st.button("ðŸ“Š Breadth", help="Summarize overall performance", use_container_width=True):
            quick_prompt = "Summarize today's performance across all my tracked stocks."
    with chip_cols[3]:
        if st.button("âš¡ Volume Leader", help="Find most actively traded stock", use_container_width=True):
            quick_prompt = "Which tracked stock has the highest trading volume today?"

    # Display Chat History
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and message.get("provider"):
                msg_time = message.get("time", "")
                time_badge = f" Â· {msg_time}" if msg_time else ""
                st.markdown(
                    f"""<div class="chat-message-meta">âš¡ {message['provider']}{time_badge}</div>""",
                    unsafe_allow_html=True,
                )

    # Chat Input Box
    user_input = st.chat_input("Ask about tracked stocks, price spreads, or volume...")
    prompt_to_send = user_input or quick_prompt

    if prompt_to_send:
        # Append user message
        st.session_state.chat_messages.append(
            {"role": "user", "content": prompt_to_send, "time": now_str}
        )

        # Query Assistant
        with st.chat_message("assistant"):
            with st.spinner("Analyzing live market telemetry..."):
                quotes = st.session_state.get("cached_quotes", {})
                reply, provider = query_assistant(prompt_to_send, selected_symbols, quotes)

        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": reply,
                "provider": provider,
                "time": time.strftime("%I:%M %p"),
            }
        )
        st.rerun()

    # Footer Guardrail Note
    st.markdown(
        """
        <div class="chat-footer-disclaimer">
            ðŸ”’ Financial telemetry & educational analytics Â· Strictly grounded in your selected watchlist.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_theme_styles(theme: str) -> None:
    """Apply CSS styles for the selected theme."""
    st.markdown(build_theme_css(theme), unsafe_allow_html=True)


def render_dashboard_app() -> None:
    """Main application runner."""
    st.set_page_config(
        page_title="StockPulse Â· Market Intelligence",
        page_icon="ðŸ“ˆ",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Initialize theme if not present
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "Midnight Navy"
    selected_symbols = []

    # Apply active theme styling dynamically
    render_theme_styles(st.session_state.get("theme_mode", "Midnight Navy"))
    # Render the global multi-market research workspace
    render_research_dashboard()

    # Floating AI Assistant popover
    with st.popover(
        "AI",
        icon="âœ¨",
        type="secondary",
        key="assistant_launcher",
        help="Open the StockPulse AI Financial Assistant",
    ):
        render_ai_assistant(selected_symbols)


if __name__ == "__main__":
    render_dashboard_app()






