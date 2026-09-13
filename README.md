# 📈 Stock Tracker App

An interactive real-time stock price tracker and dashboard built with Python and Streamlit for educational purposes.

---

## ✨ Features
- **Live Price Updates**: Automatically fetches and updates stock prices via Yahoo Finance every 5 seconds.
- **Interactive Web Dashboard**: Built with Streamlit, providing real-time metric cards and market data tables.
- **Stock Selection**: Customize stocks dynamically from the sidebar.
- **Terminal CLI Mode**: Includes a terminal ticker mode for viewing live prices directly in the console.

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

---

## 📁 Project Structure

```text
Stock_Tracker_App/
├── src/
│   ├── __init__.py       # Package marker
│   ├── tracker.py        # Yahoo Finance stock price fetching logic
│   └── dashboard.py      # Streamlit web dashboard components
│
├── main.py               # Main entry point for Streamlit Web Dashboard
├── cli.py                # Entry point for Terminal CLI Tracker
├── requirements.txt      # Python dependencies (streamlit)
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

---

## 📄 License
This project is created for educational demonstration.
