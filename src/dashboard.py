import streamlit as st

from src.tracker import REFRESH_SECONDS, SYMBOLS, get_prices


st.set_page_config(page_title="Stock Tracker App", page_icon="📈", layout="wide")


@st.cache_data(ttl=REFRESH_SECONDS - 1, show_spinner=False)
def load_prices(symbols):
    return get_prices(symbols)


def render_dashboard():
    st.title("📈 Stock Tracker App")
    st.caption(
        f"Latest available prices · automatically refreshed every {REFRESH_SECONDS} seconds"
    )

    selected_symbols = st.sidebar.multiselect(
        "Stocks", options=SYMBOLS, default=list(SYMBOLS)
    )

    if not selected_symbols:
        st.info("Select at least one stock from the sidebar.")
        return

    try:
        prices = load_prices(tuple(selected_symbols))
    except Exception as error:
        st.error(f"Unable to retrieve prices: {error}")
        return

    columns = st.columns(len(prices))
    for column, (symbol, (price, currency)) in zip(columns, prices.items()):
        with column:
            st.metric(symbol, f"{currency} {price:.2f}")

    st.subheader("Market overview")
    st.dataframe(
        [
            {"Symbol": symbol, "Price": round(price, 2), "Currency": currency}
            for symbol, (price, currency) in prices.items()
        ],
        hide_index=True,
        use_container_width=True,
    )


@st.fragment(run_every=f"{REFRESH_SECONDS}s")
def live_dashboard():
    render_dashboard()


live_dashboard()
