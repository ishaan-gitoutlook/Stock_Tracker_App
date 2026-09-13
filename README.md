# 📈 Stock Tracker App

An interactive real-time stock price tracker and financial dashboard built with Python and Streamlit for educational purposes.

---

## ✨ Features
- **Concurrent Live Updates**: Fast, asynchronous stock quotes from Yahoo Finance fetched in parallel via `ThreadPoolExecutor`.
- **Interactive Metric Cards**: Displays real-time prices, currency, company names, and daily price change + percentage change ($\Delta$).
- **Market Overview Table**: Detailed data table including daily price range (Low - High), trading volume, and net movement.
- **Dynamic Ticker Search**: Add any global stock ticker symbol directly through the sidebar.
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

#### Web Dashboard (Streamlit):
```bash
streamlit run main.py
```

#### Terminal CLI Mode:
```bash
python cli.py
```

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
│   ├── tracker.py        # Core financial data models & parallel Yahoo Finance fetcher
│   └── dashboard.py      # Streamlit web dashboard components & UI layout
├── tests/
│   ├── __init__.py       # Test package marker
│   └── test_tracker.py   # Unit tests for calculations, parsing, and error handling
├── main.py               # Main entry point for Streamlit Web Dashboard
├── cli.py                # Entry point for Terminal CLI Tracker
├── requirements.txt      # Python dependencies (streamlit)
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

---

## 📄 License
This project is created for educational demonstration.
