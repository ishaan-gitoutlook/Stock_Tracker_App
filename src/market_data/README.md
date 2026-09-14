# Market Data Service

Local development uses SQLite by default. Production should set `DATABASE_URL`
to PostgreSQL and run the API separately from Streamlit.

```powershell
pip install -r requirements.txt
$env:DATABASE_URL = "sqlite:///./market_data.db"
$env:MARKET_DATA_API_TOKEN = "local-market-data-token"
uvicorn src.market_data.api:app --reload --port 8001
```

The development EODHD connector can seed an exchange catalog:

```powershell
$env:EODHD_API_KEY = "your-development-key"
python -m src.market_data.worker listings NSE
python -m src.market_data.worker listings BSE
```

Configure the dashboard with `MARKET_DATA_API_URL=http://127.0.0.1:8001`
and the matching `MARKET_DATA_API_TOKEN`. Replace `EODHDSource` with a
licensed exchange/vendor source before production redistribution.
