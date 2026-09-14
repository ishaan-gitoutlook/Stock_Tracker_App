"""Streamlit web dashboard with live quotes, multi-market stock listings, and AI copilot."""

import io
import time
from typing import Dict, List, Optional, Tuple

import pandas as pd
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
from src.universes import (
    LABEL_TO_UNIVERSE,
    LISTING_DISPLAY_LABELS,
    MARKET_UNIVERSES,
    get_ticker_options,
)
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


def get_currency_symbol(currency_code: str) -> str:
    """Map currency code to recognizable currency symbol."""
    currency_map = {
        "USD": "$",
        "INR": "₹",
        "GBP": "£",
        "EUR": "€",
        "JPY": "¥",
        "CAD": "C$",
        "AUD": "A$",
        "CHF": "CHF",
    }
    return currency_map.get(currency_code.upper(), currency_code)


def render_sidebar() -> Tuple[str, List[str]]:
    """Render sidebar filters, stock listing selection, and custom ticker form."""
    if "available_symbols" not in st.session_state:
        st.session_state.available_symbols = list(DEFAULT_SYMBOLS)

    if "active_universe" not in st.session_state:
        st.session_state.active_universe = "Fortune 500"

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

        # Theme selection
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

        st.header("Stock Listings & Exchanges")

        # Build options for stock listings
        universe_keys = list(MARKET_UNIVERSES.keys()) + ["My Watchlist"]
        listing_options = [
            LISTING_DISPLAY_LABELS.get(k, k) if k != "My Watchlist" else "⭐ My Custom Watchlist"
            for k in universe_keys
        ]

        current_active = st.session_state.get("active_universe", "Fortune 500")
        current_active_label = (
            LISTING_DISPLAY_LABELS.get(current_active, current_active)
            if current_active != "My Watchlist"
            else "⭐ My Custom Watchlist"
        )
        try:
            active_idx = listing_options.index(current_active_label)
        except ValueError:
            active_idx = 0

        selected_label = st.selectbox(
            "Select Market Listing",
            options=listing_options,
            index=active_idx,
            help="Switch between US, Indian (NSE/BSE), UK, German, or Global Megacap listings.",
            key="sidebar_listing_select",
        )

        # Resolve selected label back to key
        if selected_label == "⭐ My Custom Watchlist":
            selected_universe = "My Watchlist"
        else:
            selected_universe = LABEL_TO_UNIVERSE.get(selected_label, selected_label)

        st.session_state.active_universe = selected_universe

        # Get constituent ticker options for chosen listing
        ticker_options = get_ticker_options(
            selected_universe, st.session_state.available_symbols
        )

        # Quick preset selection buttons
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            if st.button("Top 4", use_container_width=True, help="Track first 4 stocks in listing"):
                st.session_state[f"tracked_{selected_universe}"] = ticker_options[:4]
                st.rerun()
        with col_p2:
            if st.button("Top 8", use_container_width=True, help="Track first 8 stocks in listing"):
                st.session_state[f"tracked_{selected_universe}"] = ticker_options[:8]
                st.rerun()
        with col_p3:
            if st.button("All", use_container_width=True, help="Track all stocks in listing"):
                st.session_state[f"tracked_{selected_universe}"] = ticker_options[:]
                st.rerun()

        default_selection = st.session_state.get(
            f"tracked_{selected_universe}", ticker_options[:min(4, len(ticker_options))]
        )
        # Ensure default items are valid in current ticker options
        valid_defaults = [s for s in default_selection if s in ticker_options]
        if not valid_defaults and ticker_options:
            valid_defaults = ticker_options[:min(4, len(ticker_options))]

        selected_symbols: List[str] = st.multiselect(
            "Constituent Stocks to Track",
            options=ticker_options,
            default=valid_defaults,
            key=f"multiselect_{selected_universe}",
        )
        st.session_state[f"tracked_{selected_universe}"] = selected_symbols

        st.divider()
        st.subheader("Add Custom Symbol")
        with st.form("add_ticker_form", clear_on_submit=True):
            new_ticker = st.text_input(
                "Add Ticker Symbol", placeholder="e.g. NVDA, RELIANCE.NS, BP.L, SAP.DE"
            ).strip().upper()
            add_button = st.form_submit_button("Add Symbol to Watchlist")
            if add_button and new_ticker:
                if new_ticker not in st.session_state.available_symbols:
                    st.session_state.available_symbols.append(new_ticker)
                    st.success(f"Added {new_ticker}!")
                    st.rerun()
                else:
                    st.info(f"{new_ticker} is already in your symbols list.")

        st.divider()
        if st.button("🔄 Refresh Quotes Now", use_container_width=True):
            load_prices.clear()
            st.rerun()
        st.caption("Auto-syncs live financial quotes from global exchanges.")

    return selected_universe, selected_symbols


def render_live_market(selected_universe: str, selected_symbols: List[str]) -> None:
    """Render live market metrics, stock listing switcher, charts, and data overview."""
    universe_label = (
        LISTING_DISPLAY_LABELS.get(selected_universe, selected_universe)
        if selected_universe != "My Watchlist"
        else "⭐ My Custom Watchlist"
    )

    # Top Listing Switcher Pills right on the page for instant access
    st.markdown("### 🌐 Global Stock Listings")
    all_keys = list(MARKET_UNIVERSES.keys()) + ["My Watchlist"]
    display_pills = [
        LISTING_DISPLAY_LABELS.get(k, k) if k != "My Watchlist" else "⭐ Custom Watchlist"
        for k in all_keys
    ]

    current_idx = all_keys.index(selected_universe) if selected_universe in all_keys else 0

    chosen_display = st.radio(
        "Select Stock Listing to View:",
        options=display_pills,
        index=current_idx,
        horizontal=True,
        key="main_listing_radio",
        help="Quickly view stocks listed on US, Indian, UK, German, or Global exchanges.",
    )

    chosen_key = (
        "My Watchlist"
        if chosen_display == "⭐ Custom Watchlist"
        else LABEL_TO_UNIVERSE.get(chosen_display, chosen_display)
    )

    if chosen_key != selected_universe:
        st.session_state.active_universe = chosen_key
        st.rerun()

    if not selected_symbols:
        st.markdown(
            f"""
            <div class="hero-panel">
                <div class="hero-copy">
                    <div class="eyebrow"><span class="live-dot"></span> LIVE MARKET INTELLIGENCE</div>
                    <h1>{universe_label}</h1>
                    <p>Track live momentum, compare performance, and analyze price spreads across global stock listings.</p>
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
        st.info(f"No stocks currently selected in **{universe_label}**. Please choose stocks from the sidebar to start live tracking.")
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
                <h1>{universe_label}</h1>
                <p>Tracking live quotes and intraday performance across global listings.</p>
            </div>
            <div class="hero-stats-row">
                <div class="hero-stat-card">
                    <strong>{len(selected_symbols)}</strong>
                    <span>Tracked</span>
                </div>
                <div class="hero-stat-card">
                    <strong>{gainers_count}G · {decliners_count}D</strong>
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
        st.warning(f"Could not retrieve live data for: {', '.join(sorted(missing_symbols))}")

    # Section 1: KPI Cards for Tracked Stocks
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

            curr_sym = get_currency_symbol(quote_data.currency)
            st.metric(
                label=f"{sym} · {quote_data.name}",
                value=f"{curr_sym} {quote_data.price:,.2f}",
                delta=delta_str,
            )

    # Section 2: Relative Performance Bar Chart
    perf_data = {
        sym: quote_data.change_percent
        for sym, quote_data in quotes.items()
        if quote_data.change_percent is not None
    }
    if perf_data:
        st.markdown(
            """
            <div class="section-heading">
                <div class="section-kicker">MOMENTUM RADAR</div>
                <div class="section-title">Intraday change comparison (%)</div>
                <div class="section-subtitle">Relative percentage movement across tracked stocks</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        df_perf = pd.DataFrame(
            list(perf_data.items()), columns=["Ticker", "Change (%)"]
        ).set_index("Ticker")
        st.bar_chart(df_perf, use_container_width=True)

    # Section 3: Comprehensive Overview Table
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
        curr_sym = get_currency_symbol(quote_data.currency)
        if quote_data.day_low is not None and quote_data.day_high is not None:
            day_range = f"{curr_sym}{quote_data.day_low:,.2f} - {curr_sym}{quote_data.day_high:,.2f}"
        table_data.append(
            {
                "Symbol": sym,
                "Company": quote_data.name,
                "Price": f"{curr_sym} {quote_data.price:,.2f}",
                "Change": f"{quote_data.change:+.2f}" if quote_data.change is not None else "N/A",
                "Change (%)": f"{quote_data.change_percent:+.2f}%" if quote_data.change_percent is not None else "N/A",
                "Day Range": day_range,
                "Volume": f"{quote_data.volume:,}" if quote_data.volume else "N/A",
            }
        )
    st.dataframe(table_data, hide_index=True, use_container_width=True)

    timestamp = time.strftime("%H:%M:%S")
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.caption(f"Last updated: {timestamp} · Auto-refreshing every {REFRESH_SECONDS}s · Data feed: {source}")
    with col_t2:
        df_export = pd.DataFrame(table_data)
        csv_buffer = io.StringIO()
        df_export.to_csv(csv_buffer, index=False)
        st.download_button(
            "📥 Download Table CSV",
            data=csv_buffer.getvalue(),
            file_name=f"{selected_universe.lower().replace(' ', '_')}_quotes.csv",
            mime="text/csv",
            use_container_width=True,
        )


def render_ai_assistant(selected_symbols: List[str]) -> None:
    """Render the stock performance AI assistant inside the floating chat popover."""
    now_str = time.strftime("%I:%M %p")

    # Header with title, live status, and action buttons
    header_cols = st.columns([0.8, 0.2])
    with header_cols[0]:
        st.markdown(
            """
            <div class="chat-header">
                <div class="chat-header-left">
                    <div class="chat-avatar">✨</div>
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
        if st.button("🧹 Clear", help="Reset conversation history", use_container_width=True):
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
                <span style="color: var(--ui-bearish); font-size: 0.72rem;">No symbols selected. Select stocks from the listing for live analysis.</span>
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
        if st.button("🚀 Top Gainer", help="Find the stock with largest gain", use_container_width=True):
            quick_prompt = "Which tracked stock had the largest increase today?"
    with chip_cols[1]:
        if st.button("🔻 Biggest Drop", help="Find the stock with largest decline", use_container_width=True):
            quick_prompt = "Which stock had the largest drop today?"
    with chip_cols[2]:
        if st.button("📊 Breadth", help="Summarize overall performance", use_container_width=True):
            quick_prompt = "Summarize today's performance across all my tracked stocks."
    with chip_cols[3]:
        if st.button("⚡ Volume Leader", help="Find most actively traded stock", use_container_width=True):
            quick_prompt = "Which tracked stock has the highest trading volume today?"

    # Display Chat History
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and message.get("provider"):
                msg_time = message.get("time", "")
                time_badge = f" · {msg_time}" if msg_time else ""
                st.markdown(
                    f"""<div class="chat-message-meta">⚡ {message['provider']}{time_badge}</div>""",
                    unsafe_allow_html=True,
                )

    # Chat Input Box
    user_input = st.chat_input("Ask about tracked stocks, price spreads, or volume...")
    prompt_to_send = user_input or quick_prompt

    if prompt_to_send:
        st.session_state.chat_messages.append(
            {"role": "user", "content": prompt_to_send, "time": now_str}
        )

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
            🔒 Financial telemetry & educational analytics · Strictly grounded in your selected watchlist.
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
        page_title="StockPulse · Market Intelligence",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Initialize theme if not present
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "Midnight Navy"

    # Render sidebar and get active listing and tracked symbols
    selected_universe, selected_symbols = render_sidebar()

    # Apply active theme styling dynamically
    render_theme_styles(st.session_state.get("theme_mode", "Midnight Navy"))

    # Top-level workspace navigation tabs
    tab_live, tab_research = st.tabs([
        "📈 Live Market Tracker & Listings",
        "🔬 In-Depth Fundamentals Research",
    ])

    with tab_live:
        render_live_market(selected_universe, selected_symbols)

    with tab_research:
        render_research_dashboard()

    # Floating AI Assistant popover
    with st.popover(
        "AI",
        icon="✨",
        type="secondary",
        key="assistant_launcher",
        help="Open the StockPulse AI Financial Assistant",
    ):
        render_ai_assistant(selected_symbols)


if __name__ == "__main__":
    render_dashboard_app()
