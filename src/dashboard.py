"""Streamlit web dashboard with live quotes and a stock performance assistant."""

import time
from typing import Dict, List, Tuple

import streamlit as st

from src.api_client import APIClientError, fetch_quotes, send_chat_message
from src.assistant import ask_assistant
from src.tracker import DEFAULT_SYMBOLS, REFRESH_SECONDS, StockQuote, get_prices
from src.universes import MARKET_UNIVERSES, get_ticker_options


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
                <div>
                    <div class="brand-name">StockPulse</div>
                    <div class="brand-caption">MARKET INTELLIGENCE</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
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
        if st.button("Refresh Quotes Now", use_container_width=True):
            load_prices.clear()
            st.rerun()
        st.caption("Choose a universe, select entities, or add custom symbols.")

    st.session_state.current_selected_symbols = selected_symbols
    return selected_symbols


@st.fragment(run_every=f"{REFRESH_SECONDS}s")
def render_live_market(selected_symbols: List[str]) -> None:
    """Render live market metrics and the overview table."""
    st.markdown(
        f"""
        <div class="hero-panel">
            <div class="hero-copy">
                <div class="eyebrow"><span class="live-dot"></span> LIVE MARKET INTELLIGENCE</div>
                <h1>Market Pulse</h1>
                <p>Track momentum, compare performance, and stay close to the market.</p>
            </div>
            <div class="hero-stat">
                <strong>{len(selected_symbols)}</strong>
                <span>tracked entities</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not selected_symbols:
        st.info("Please select or add at least one stock from the sidebar.")
        return

    try:
        quotes, source = load_prices(tuple(selected_symbols))
    except Exception as err:
        st.error(f"Unable to retrieve stock data: {err}")
        return

    st.session_state.cached_quotes = quotes
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
            <div class="section-subtitle">Your selected entities at a glance</div>
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
                label=f"{sym} · {quote_data.name}",
                value=f"{quote_data.currency} {quote_data.price:.2f}",
                delta=delta_str,
            )

    st.markdown(
        """
        <div class="section-heading overview-heading">
            <div class="section-kicker">MARKET DATA</div>
            <div class="section-title">Market overview</div>
            <div class="section-subtitle">Intraday price movement and liquidity</div>
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
    st.caption(f"Last updated: {timestamp} · Auto-refreshing every {REFRESH_SECONDS}s · Source: {source}")


def render_ai_assistant(selected_symbols: List[str]) -> None:
    """Render the stock-only assistant inside the floating chat popover."""
    st.subheader("Stock Assistant")
    st.caption("Ask only about tracked stocks and their performance.")

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Ask me about your tracked stocks and their performance.", "provider": "Assistant"}
        ]

    prompt_cols = st.columns(3)
    quick_prompt = None
    with prompt_cols[0]:
        if st.button("Top gainer", use_container_width=True):
            quick_prompt = "Which tracked stock had the largest increase today?"
    with prompt_cols[1]:
        if st.button("Biggest decline", use_container_width=True):
            quick_prompt = "Which stock had the largest drop today?"
    with prompt_cols[2]:
        if st.button("Clear chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("provider") and message["role"] == "assistant":
                st.caption(f"Engine: {message['provider']}")

    user_input = st.chat_input("Ask about tracked stock performance...")
    prompt_to_send = user_input or quick_prompt
    if not prompt_to_send:
        return

    st.session_state.chat_messages.append({"role": "user", "content": prompt_to_send})
    with st.chat_message("user"):
        st.markdown(prompt_to_send)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing tracked stock performance..."):
            quotes = st.session_state.get("cached_quotes", {})
            reply, provider = query_assistant(prompt_to_send, selected_symbols, quotes)
            st.markdown(reply)
            st.caption(f"Engine: {provider}")

    st.session_state.chat_messages.append(
        {"role": "assistant", "content": reply, "provider": provider}
    )
    if quick_prompt:
        st.rerun()


def render_dashboard_app() -> None:
    """Main application runner."""
    st.set_page_config(page_title="Stock Tracker App", page_icon="💹", layout="wide")
    st.markdown(
        """
        <style>
        :root {
            --stock-indigo: #5b5ce2;
            --stock-cyan: #18c8c8;
            --stock-pink: #e85aad;
        }
        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 8% 0%, rgba(91, 92, 226, 0.16), transparent 30rem),
                radial-gradient(circle at 100% 20%, rgba(24, 200, 200, 0.12), transparent 28rem);
        }
        [data-testid="stHeader"] {
            background: transparent;
        }
        h1 {
            background: linear-gradient(90deg, var(--stock-indigo), var(--stock-cyan), var(--stock-pink));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-weight: 800;
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(91, 92, 226, 0.14), rgba(24, 200, 200, 0.07));
            border-right: 1px solid rgba(91, 92, 226, 0.2);
        }
        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, rgba(91, 92, 226, 0.16), rgba(24, 200, 200, 0.08));
            border: 1px solid rgba(91, 92, 226, 0.24);
            border-radius: 1rem;
            padding: 1rem;
            box-shadow: 0 0.5rem 1.5rem rgba(32, 35, 84, 0.1);
            transition: transform 160ms ease, box-shadow 160ms ease;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 0.8rem 1.8rem rgba(32, 35, 84, 0.18);
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(91, 92, 226, 0.2);
            border-radius: 1rem;
            overflow: hidden;
        }
        div[data-testid="stPopover"] {
            position: fixed;
            right: 1rem;
            bottom: 1rem;
            z-index: 999999;
        }
        div[data-testid="stPopover"] > button {
            border-radius: 999px;
            width: 2.35rem;
            height: 2.35rem;
            min-height: 2.35rem;
            min-width: 2.35rem;
            padding: 0;
            border: 0;
            color: white;
            background: linear-gradient(135deg, var(--stock-indigo), var(--stock-pink));
            box-shadow: 0 0.35rem 1rem rgba(91, 92, 226, 0.4);
            font-size: 0.95rem;
            line-height: 1;
            transition: transform 160ms ease, box-shadow 160ms ease;
            animation: assistant-pulse 3s ease-in-out infinite;
        }
        div[data-testid="stPopover"] > button:hover {
            transform: scale(1.08);
            box-shadow: 0 0.5rem 1.2rem rgba(232, 90, 173, 0.45);
        }
        @keyframes assistant-pulse {
            0%, 100% { box-shadow: 0 0.35rem 1rem rgba(91, 92, 226, 0.35); }
            50% { box-shadow: 0 0.35rem 1.25rem rgba(24, 200, 200, 0.55); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1480px;
            padding-top: 2.5rem;
            padding-bottom: 5rem;
        }
        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 5% 0%, rgba(91, 92, 226, 0.12), transparent 32rem),
                radial-gradient(circle at 100% 12%, rgba(24, 200, 200, 0.1), transparent 30rem),
                #f8faff;
        }
        [data-testid="stHeader"] { background: transparent; }
        h1 { margin: 0 !important; font-size: clamp(2.3rem, 4vw, 4.4rem) !important; letter-spacing: -0.06em; }
        h2, h3 { color: #0b1220 !important; }
        .hero-panel {
            display: flex; align-items: flex-end; justify-content: space-between; gap: 2rem;
            margin-bottom: 2.25rem; padding: 2rem 2.25rem; border: 1px solid rgba(91,92,226,.2);
            border-radius: 1.5rem; color: white;
            background: linear-gradient(120deg, #111936 0%, #24245b 52%, #087e8b 130%);
            box-shadow: 0 1.25rem 3rem rgba(35,43,92,.2); overflow: hidden; position: relative;
        }
        .hero-panel::after { content: ""; position: absolute; width: 18rem; height: 18rem; right: -4rem; top: -8rem; border-radius: 50%; background: rgba(255,255,255,.1); }
        .hero-copy, .hero-stat { position: relative; z-index: 1; }
        .hero-copy p { margin: .6rem 0 0; color: rgba(255,255,255,.72); font-size: 1rem; }
        .hero-panel h1 { color: white !important; }
        .eyebrow, .section-kicker, .brand-caption { font-size: .68rem; font-weight: 800; letter-spacing: .16em; text-transform: uppercase; }
        .eyebrow { color: #8df4e6; }
        .live-dot { display: inline-block; width: .48rem; height: .48rem; margin-right: .4rem; border-radius: 50%; background: #65f5b0; box-shadow: 0 0 .6rem #65f5b0; }
        .hero-stat { min-width: 9rem; padding: 1rem 1.15rem; border: 1px solid rgba(255,255,255,.18); border-radius: 1rem; background: rgba(255,255,255,.1); backdrop-filter: blur(1rem); }
        .hero-stat strong, .hero-stat span { display: block; }
        .hero-stat strong { font-size: 2rem; line-height: 1; }
        .hero-stat span { margin-top: .35rem; color: rgba(255,255,255,.7); font-size: .78rem; }
        .section-heading { margin: 1rem 0 1.1rem; }
        .overview-heading { margin-top: 2.75rem; }
        .section-kicker { color: #5b5ce2; }
        .section-title { margin-top: .2rem; color: #0b1220; font-size: 1.7rem; font-weight: 800; letter-spacing: -.03em; }
        .section-subtitle { color: #718096; font-size: .9rem; }
        .sidebar-brand { display: flex; align-items: center; gap: .7rem; margin: .2rem 0 2rem; }
        .brand-mark { display: grid; width: 2.35rem; height: 2.35rem; place-items: center; border-radius: .75rem; color: white; background: linear-gradient(135deg,#5b5ce2,#18c8c8); font-size: .8rem; font-weight: 900; }
        .brand-name { color: #0b1220; font-size: 1.1rem; font-weight: 850; }
        .brand-caption { color: #718096; font-size: .52rem; letter-spacing: .13em; }
        section[data-testid="stSidebar"] { background: linear-gradient(180deg,#f0f2ff,#f8faff 70%); border-right: 1px solid rgba(91,92,226,.17); }
        div[data-testid="stMetric"] { min-height: 8rem; background: rgba(255,255,255,.76); border: 1px solid rgba(91,92,226,.17); border-radius: 1rem; padding: 1rem; box-shadow: 0 .55rem 1.5rem rgba(32,35,84,.07); transition: transform 160ms ease, box-shadow 160ms ease; }
        div[data-testid="stMetric"]:hover { transform: translateY(-3px); box-shadow: 0 .8rem 1.8rem rgba(32,35,84,.18); }
        div[data-testid="stDataFrame"] { border: 1px solid rgba(91,92,226,.17); border-radius: 1rem; overflow: hidden; box-shadow: 0 .55rem 1.5rem rgba(32,35,84,.06); }
        .st-key-assistant_launcher { position: fixed !important; right: 1.25rem; bottom: 1.25rem; z-index: 999999; }
        .st-key-assistant_launcher > div > button { width: 3.15rem; height: 3.15rem; min-width: 3.15rem; min-height: 3.15rem; padding: .7rem; border: 3px solid white; border-radius: 999px; color: white; background: linear-gradient(135deg,#5b5ce2,#e85aad); box-shadow: 0 .5rem 1.4rem rgba(91,92,226,.38); font-size: 1.05rem; line-height: 1; transition: transform 160ms ease, box-shadow 160ms ease; animation: assistant-pulse 3s ease-in-out infinite; }
        .st-key-assistant_launcher > div > button:hover { transform: scale(1.08); box-shadow: 0 .5rem 1.2rem rgba(232,90,173,.45); }
        @keyframes assistant-pulse { 0%,100% { box-shadow: 0 .35rem 1rem rgba(91,92,226,.35); } 50% { box-shadow: 0 .35rem 1.25rem rgba(24,200,200,.55); } }
        @media (max-width: 700px) { .hero-panel { align-items: flex-start; flex-direction: column; padding: 1.4rem; } .hero-stat { min-width: 7rem; } }
        [data-testid="stMetricLabel"], [data-testid="stMetricValue"], [data-testid="stMetricDelta"] { color: #0b1220 !important; }
        section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] .stMarkdown { color: #26324a !important; }
        .st-key-assistant_launcher, .st-key-assistant_launcher > div, .st-key-assistant_launcher [data-testid="stPopover"] { width: max-content !important; min-width: 0 !important; max-width: max-content !important; background: transparent !important; border: 0 !important; }
        .st-key-assistant_launcher button[data-testid="stPopoverButton"], .st-key-assistant_launcher > div > button { width: 3.15rem !important; min-width: 3.15rem !important; max-width: 3.15rem !important; height: 3.15rem !important; min-height: 3.15rem !important; padding: 0 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    selected_symbols = render_sidebar()
    render_live_market(selected_symbols)
    with st.popover(
        "AI",
        icon="💬",
        type="secondary",
        key="assistant_launcher",
        help="Open the stock performance assistant",
    ):
        render_ai_assistant(selected_symbols)


if __name__ == "__main__":
    render_dashboard_app()
