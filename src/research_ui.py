"""Multi-market Streamlit research workspace."""
import json
import streamlit as st
from src.api_client import APIClientError, configured_market_data_url, fetch_market_listings, search_market_instruments
from src.research import EODHDProvider, ResearchProviderError, MARKET_EXCHANGES, Instrument


PROVIDER_EXCHANGES = {
    "India": {"NSE": "NSE", "BSE": "BSE"},
    "United States": {"NYSE": "US", "NASDAQ": "US", "AMEX": "US"},
    "Europe": {"LSE": "LSE", "XETRA": "XETRA", "EURONEXT": "EU", "SIX": "SIX", "BME": "BME", "NASDAQ NORDIC": "NORDIC"},
}


@st.cache_data(ttl=86400, show_spinner=False)
def load_exchange_catalog(api_key: str, provider_exchange: str) -> list[Instrument]:
    """Cache a full active exchange catalog for the current provider key."""
    if configured_market_data_url():
        return fetch_market_listings(provider_exchange)
    return EODHDProvider(api_key=api_key).exchange_symbols(provider_exchange)

def _symbol(item: Instrument) -> str:
    return item.symbol if '.' in item.symbol else (item.symbol + '.' + item.exchange if item.exchange else item.symbol)

def render_research_tab(market: str) -> None:
    watch_key = 'watchlist_' + market
    if watch_key not in st.session_state: st.session_state[watch_key] = []
    st.subheader(market + ' market')
    st.caption('Supported exchanges: ' + ', '.join(MARKET_EXCHANGES[market]) + ' · Data is delayed/near-live according to provider plan.')
    provider = EODHDProvider()
    internal_api = configured_market_data_url()
    if not provider.api_key and not internal_api:
        st.warning('Set MARKET_DATA_API_URL and MARKET_DATA_API_TOKEN for the normalized provider, or EODHD_API_KEY for development mode.')
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: query = st.text_input('Search symbol or company', key='query_' + market, placeholder='e.g. Reliance, AAPL, SAP')
    with c2: exchange = st.selectbox('Exchange', ['All'] + list(MARKET_EXCHANGES[market]), key='exchange_' + market)
    with c3:
        st.write('')
        search = st.button('Search', key='search_' + market)
    catalog_exchange = PROVIDER_EXCHANGES[market].get(exchange, exchange)
    if (provider.api_key or internal_api) and exchange != 'All':
        if st.button('Load full exchange listing', key='catalog_button_' + market):
            try:
                catalog = load_exchange_catalog(provider.api_key, catalog_exchange)
                st.session_state['catalog_' + market] = catalog
                st.success(f'Loaded {len(catalog):,} active instruments from {exchange}.')
            except ResearchProviderError as err:
                st.error(str(err))
        catalog = st.session_state.get('catalog_' + market, [])
        if catalog:
            catalog_labels = {f'{item.symbol} · {item.name} · {item.exchange}': item for item in catalog}
            catalog_label = st.selectbox('All active exchange listings', list(catalog_labels), key='catalog_select_' + market)
            if st.button('Add selected listing', key='catalog_add_' + market):
                value = _symbol(catalog_labels[catalog_label])
                if value not in st.session_state[watch_key]:
                    st.session_state[watch_key].append(value)
                    st.session_state['selected_' + market] = value
    if search and query.strip() and (provider.api_key or internal_api):
        try:
            if internal_api:
                st.session_state['results_' + market] = search_market_instruments(query.strip(), None if exchange == 'All' else exchange)
            else:
                st.session_state['results_' + market] = provider.search(query.strip(), market, None if exchange == 'All' else exchange)
        except (ResearchProviderError, APIClientError) as err: st.error(str(err))
    results = st.session_state.get('results_' + market, [])
    if results:
        labels = {f'{x.symbol} · {x.name} · {x.exchange}': x for x in results[:100]}
        label = st.selectbox('Search results', list(labels), key='result_' + market)
        if st.button('Add to watchlist', key='add_' + market):
            value = _symbol(labels[label])
            if value not in st.session_state[watch_key]: st.session_state[watch_key].append(value)
    watchlist = st.session_state[watch_key]
    if not watchlist:
        st.info('Search for an instrument and add it to this market watchlist.')
        return
    selected = st.selectbox('Watchlist', watchlist, key='selected_' + market)
    a, b, c = st.columns(3)
    with a:
        if st.button('Remove', key='remove_' + market):
            st.session_state[watch_key] = [x for x in watchlist if x != selected]; st.rerun()
    with b: st.download_button('Export JSON', json.dumps(watchlist, indent=2), market.lower().replace(' ', '_') + '_watchlist.json', key='export_' + market)
    with c:
        upload = st.file_uploader('Import JSON', type='json', key='import_' + market)
        if upload:
            try:
                values = json.load(upload)
                if isinstance(values, list): st.session_state[watch_key] = list(dict.fromkeys(str(x).upper() for x in values)); st.rerun()
            except (json.JSONDecodeError, UnicodeDecodeError): st.error('Invalid watchlist JSON.')
    if not provider.api_key: return
    try: profile = provider.fundamentals(selected)
    except ResearchProviderError as err: st.error(str(err)); return
    st.markdown(f'#### {profile.name} ({profile.symbol})')
    st.caption(f'{profile.exchange or "Exchange unavailable"} · {profile.currency or "Currency unavailable"} · Source: {profile.source} · As of: {profile.as_of or "Unavailable"}')
    quote = profile.quote
    st.dataframe([{'Price': quote.get('close', 'N/A'), 'Change %': quote.get('change_p', 'N/A'), 'High': quote.get('high', 'N/A'), 'Low': quote.get('low', 'N/A'), 'Volume': quote.get('volume', 'N/A')}], hide_index=True, use_container_width=True)
    tabs = st.tabs(['Valuation', 'Profitability', 'Statements', 'Dividends', 'Chart', 'Company'])
    with tabs[0]: st.dataframe([profile.valuation or {'Status': 'Unavailable'}], hide_index=True, use_container_width=True)
    with tabs[1]: st.dataframe([profile.profitability or {'Status': 'Unavailable'}], hide_index=True, use_container_width=True)
    with tabs[2]:
        for name, value in profile.statements.items():
            st.markdown('**' + name + '**'); st.json(value)
    with tabs[3]: st.dataframe(profile.dividends or [{'Status': 'Unavailable'}], hide_index=True, use_container_width=True)
    with tabs[4]:
        period = st.selectbox('History period', ['1m', '3m', '6m', '1y', '5y'], key='period_' + market)
        try:
            points = provider.history(selected, period)
            if points:
                st.line_chart({'close': {x.date: x.close for x in points if x.close is not None}})
                st.dataframe([x.__dict__ for x in points], hide_index=True, use_container_width=True)
            else: st.info('Historical data unavailable.')
        except ResearchProviderError as err: st.error(str(err))
    with tabs[5]: st.json(profile.company or {'Status': 'Unavailable'})

def render_research_dashboard() -> None:
    st.title('Global Stock Research')
    tabs = st.tabs(['India', 'United States', 'Europe'])
    for tab, market in zip(tabs, ['India', 'United States', 'Europe']):
        with tab: render_research_tab(market)
