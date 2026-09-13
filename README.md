# 📈 Stock Tracker App

An interactive real-time stock price tracker and financial dashboard built with Python and Streamlit for educational purposes.

---

## ✨ Features
- **Concurrent Live Updates**: Fast, asynchronous stock quotes from Yahoo Finance fetched in parallel via `ThreadPoolExecutor`.
- **Interactive Metric Cards**: Displays real-time prices, currency, company names, and daily price change + percentage change ($\Delta$).
- **Market Overview Table**: Detailed data table including daily price range (Low - High), trading volume, and net movement.
- **Dynamic Ticker Search**: Add any global stock ticker symbol directly through the sidebar.
- **Market Universes**: Select tracked entities from the built-in NIFTY 500 and Fortune 500 lists.
- **Manual Refresh**: Force an immediate fresh quote fetch with the sidebar refresh button.
- **FastAPI Backend**: Exposes health, universe, and quote endpoints for frontend/API clients.
- **Auto-Refresh**: Live periodic updates every 5 seconds using Streamlit fragments without full page reloads.
- **Terminal CLI Mode**: Lightweight console ticker view with formatted output.
- **Built-in Unit Tests**: Clean test coverage using Python's standard `unittest` framework.

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/ishaan-gitoutlook/Stock_Tracker_App.git
cd Stock_Tracker_App
```

### 2. Set up virtual environment & install dependencies
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the App

#### 1. Start the FastAPI backend:
```bash
uvicorn src.api:app --reload
```

#### 2. Start the Streamlit dashboard in another terminal:
```bash
streamlit run main.py
```

#### Terminal CLI Mode:
```bash
python cli.py
```

The Streamlit client uses `http://127.0.0.1:8000` by default. Set `STOCK_API_URL` when the
backend runs elsewhere.

### 4. Run Unit Tests
```bash
python -m unittest discover tests
```

---

## 📁 Project Structure

```text
Stock_Tracker_App/
├── src/
│   ├── __init__.py       # Package marker
│   ├── api.py             # FastAPI backend and REST endpoints
│   ├── api_client.py      # Streamlit-to-FastAPI HTTP client
│   ├── universes.py       # NIFTY 500 and Fortune 500 ticker collections
│   ├── tracker.py        # Core financial data models & parallel Yahoo Finance fetcher
│   └── dashboard.py      # Streamlit web dashboard components & UI layout
├── tests/
│   ├── __init__.py       # Test package marker
│   ├── test_api_client.py # Backend client tests
│   ├── test_dashboard.py  # Universe selection tests
│   └── test_tracker.py   # Unit tests for calculations, parsing, and error handling
├── main.py               # Main entry point for Streamlit Web Dashboard
├── cli.py                # Entry point for Terminal CLI Tracker
├── requirements.txt      # Python dependencies (Streamlit, FastAPI, Uvicorn)
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

---

## 📄 License
This project is created for educational demonstration.
