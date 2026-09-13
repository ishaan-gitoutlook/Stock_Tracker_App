# 📈 Stock Tracker App

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/Tests-15%20Passing-brightgreen.svg)](tests/)
[![Architecture](https://img.shields.io/badge/Architecture-2--Tier%20Microservice-orange.svg)]()
[![License](https://img.shields.io/badge/License-Educational%20Use-lightgrey.svg)]()

A modern, full-stack real-time financial tracking dashboard and REST API built for educational purposes. Demonstrates a decoupled **2-tier microservice architecture** combining **FastAPI** for high-throughput asynchronous financial data ingestion and **Streamlit** for reactive data visualization, complete with automated fallback capabilities and interactive terminal CLI support.

---

## 📑 Table of Contents

- [System Architecture](#-system-architecture)
- [✨ Key Features](#-key-features)
- [📁 Project Structure](#-project-structure)
- [🌐 REST API Reference](#-rest-api-reference)
- [🚀 Quick Start (Local Setup)](#-quick-start-local-setup)
- [🧪 Running Automated Tests](#-running-automated-tests)
- [☁️ Cloud Deployment Guide](#️-cloud-deployment-guide)
  - [1. Deploying FastAPI to Render](#1-deploying-fastapi-to-render)
  - [2. Deploying Streamlit to Streamlit Cloud](#2-deploying-streamlit-to-streamlit-community-cloud)
  - [3. Standalone Mode (Zero-Config)](#3-standalone-mode-zero-config)
- [⚙️ Configuration & Environment Variables](#️-configuration--environment-variables)
- [📄 Educational Disclaimer](#-educational-disclaimer)

---

## 🏛️ System Architecture

The application adopts an enterprise microservice pattern with built-in resilience:

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT / PRESENTATION                    │
│                                                             │
│   Streamlit Web Dashboard            Terminal CLI Tracker   │
│       (main.py)                           (cli.py)          │
└──────────────┬──────────────────────────────────┬───────────┘
               │                                  │
    HTTP / REST│ (Configured via STOCK_API_URL)   │
               ▼                                  │
┌───────────────────────────────┐                 │
│         API BACKEND           │                 │
│      FastAPI / Uvicorn        │                 │
│      (src/api.py)             │                 │
│  - /api/v1/quotes             │                 │
│  - /api/v1/universes          │                 │
│  - /health                    │                 │
└──────────────┬────────────────┘                 │
               │                                  │
               │ (Internal Data Service)          │
               ▼                                  │
┌─────────────────────────────────────────────────┴───────────┐
│                     CORE DATA LAYER                         │
│                    (src/tracker.py)                         │
│                                                             │
│  - Parallel ThreadPoolExecutor                              │
│  - Strongly-Typed StockQuote Domain Model                   │
│  - Resilient Fault-Tolerant Symbol Ingestion                │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTPS
                               ▼
                 Yahoo Finance Financial API
```

### 🛡️ Smart Dual-Mode Fallback Design
* **Primary (FastAPI Mode):** When the FastAPI backend is running (locally or on the cloud via `STOCK_API_URL`), Streamlit consumes quotes via structured JSON endpoints.
* **Secondary (Direct Fallback Mode):** If the backend is temporarily offline or unconfigured (such as during standalone Streamlit Cloud deployment), Streamlit seamlessly switches to direct in-memory fetching without dropping connections or displaying error screens.

---

## ✨ Key Features

### 📊 Reactive Frontend (Streamlit)
- **Live Price Updates:** Real-time stock ticker quotes refreshed every 5 seconds using non-blocking Streamlit fragments (`@st.fragment`).
- **Interactive Metric Cards:** Displays company name, current market price, and colored price movement deltas ($\Delta$ with absolute value and percentage).
- **Curated Market Universes:** Filter and track major stock collections, including **NIFTY 500**, **Fortune 500**, and personal watchlists.
- **Dynamic Ticker Adder:** Search and add any valid global ticker symbol (e.g., `NVDA`, `TSLA`, `RELIANCE.NS`, `BTC-USD`) on the fly with automatic deduplication.
- **Comprehensive Market Table:** Detailed overview containing daily price range ($Low - High$), 24-hour volume, and net change.
- **Instant Manual Refresh:** Clear the UI cache on demand with a single click.

### ⚡ Asynchronous REST API (FastAPI)
- **Interactive Documentation:** Automated Swagger UI (`/docs`) and ReDoc (`/redoc`) exploring data contracts and schemas.
- **High Concurrency:** Utilizes Python's `concurrent.futures.ThreadPoolExecutor` to fetch multiple symbols simultaneously in $<0.8\text{s}$.
- **Health Checks:** Built-in `/health` probe for automated container and service monitoring.

### 💻 Command-Line Interface (CLI)
- **Terminal Price Ticker:** Lightweight console view with formatted ASCII tables and auto-clearing screens for terminal enthusiasts.

---

## 📁 Project Structure

```text
Stock_Tracker_App/
│
├── src/                                  # Modular application source code
│   ├── __init__.py                       # Package initializer
│   ├── tracker.py                        # Core domain models & parallel data fetcher
│   ├── universes.py                      # Curated market indices (NIFTY 500, Fortune 500)
│   ├── api.py                            # FastAPI REST service & route definitions
│   ├── api_client.py                     # Resilient HTTP client with secret resolution
│   └── dashboard.py                      # Streamlit UI layouts, metrics & state handling
│
├── tests/                                # Automated unit test suite
│   ├── __init__.py                       # Test package initializer
│   ├── test_tracker.py                   # Data parsing, calculations & fallback tests
│   ├── test_api_client.py                # HTTP client serialization & error handling tests
│   └── test_dashboard.py                 # Universe indexing & fallback mode tests
│
├── main.py                               # Application entry point for Streamlit Web Dashboard
├── cli.py                                # Application entry point for Terminal CLI Tracker
├── requirements.txt                      # Production & development dependencies
├── .gitignore                            # Excluded cache, environment, and IDE artifacts
├── .gitattributes                        # Cross-platform line ending normalization
└── README.md                             # Comprehensive project documentation
```

---

## 🌐 REST API Reference

When the FastAPI server is running (`http://127.0.0.1:8000`), the interactive documentation is available at:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

### Endpoints Overview

| Method | Endpoint | Description | Sample Query / Params |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | System health check and status verification | `N/A` |
| `GET` | `/api/v1/universes` | Lists all supported market index universes | `N/A` |
| `GET` | `/api/v1/quotes` | Fetches live market data for requested symbols | `?symbols=AAPL,MSFT&fresh=false` |

#### Sample Quote Response (`GET /api/v1/quotes?symbols=AAPL`)
```json
{
  "count": 1,
  "quotes": [
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "price": 242.50,
      "currency": "USD",
      "previous_close": 239.80,
      "change": 2.70,
      "change_percent": 1.13,
      "day_high": 243.20,
      "day_low": 238.90,
      "volume": 48920100
    }
  ]
}
```

---

## 🚀 Quick Start (Local Setup)

### 1. Prerequisites
- **Python 3.10+** installed on your system.
- Git installed on your system.

### 2. Clone the Repository
```bash
git clone https://github.com/ishaan-gitoutlook/Stock_Tracker_App.git
cd Stock_Tracker_App
```

### 3. Create & Activate Virtual Environment
```bash
# Windows (PowerShell):
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 5. Running the Application

You can run the project in three different ways:

#### Mode A: Full Microservices Stack (FastAPI + Streamlit)
Open two separate terminal tabs:

* **Terminal 1 (Backend API):**
  ```bash
  uvicorn src.api:app --reload --port 8000
  ```
* **Terminal 2 (Frontend Dashboard):**
  ```bash
  streamlit run main.py
  ```

#### Mode B: Standalone Web Dashboard (Direct Yahoo Finance Mode)
If you do not need the REST API running locally, simply run:
```bash
streamlit run main.py
```
*(The dashboard will automatically detect that the API is offline and safely fetch data directly).*

#### Mode C: Terminal CLI Tracker
To view live ASCII market quotes directly in your terminal console:
```bash
python cli.py
```

---

## 🧪 Running Automated Tests

The repository includes a comprehensive unit testing suite using Python's built-in `unittest` framework, validating domain logic, calculations, API serialization, and fallback mechanisms with zero external test runners required.

To execute all tests:
```bash
python -m unittest discover tests
```

Expected output:
```text
...............
----------------------------------------------------------------------
Ran 15 tests in 0.005s

OK
```

---

## ☁️ Cloud Deployment Guide

To deploy this project online so teachers and friends can access it via a public URL, use the following free setup:

### 1. Deploying FastAPI to Render
1. Sign up / log in to [render.com](https://render.com) with GitHub.
2. Click **New +** ➜ **Web Service** ➜ Select `Stock_Tracker_App`.
3. Configure the service:
   - **Name:** `stock-tracker-api`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.api:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
4. Click **Deploy Web Service**.
5. Once deployed, note down your live URL (e.g. `https://stock-tracker-api.onrender.com`).

### 2. Deploying Streamlit to Streamlit Community Cloud
1. Sign in to [share.streamlit.io](https://share.streamlit.io) with GitHub.
2. Click **Create app** ➜ select repository `ishaan-gitoutlook/Stock_Tracker_App` with branch `master` and file `main.py`.
3. Under **Advanced Settings** ➜ **Secrets**, provide your Render API URL:
   ```toml
   STOCK_API_URL = "https://your-api-name.onrender.com"
   ```
4. Click **Deploy!**

### 3. Standalone Mode (Zero-Config)
If you do not wish to host a separate Render service, simply deploy directly to Streamlit Community Cloud without configuring any secrets. The built-in fallback will activate automatically, providing 100% functionality out of the box!

---

## ⚙️ Configuration & Environment Variables

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `STOCK_API_URL` | `http://127.0.0.1:8000` | Base endpoint of the FastAPI backend. Can also be defined in Streamlit Cloud Secrets. |
| `REFRESH_SECONDS`| `5` | Polling interval for live stock quote refreshes. |
| `REQUEST_TIMEOUT`| `8` | Network timeout in seconds for upstream financial queries. |

---

## 📄 Educational Disclaimer

This project was developed strictly for **educational and demonstration purposes**. Market data is fetched from publicly available endpoints. It is not intended for live automated trading or investment advisory services.

---

## 👨‍💻 Author & Repository

- **Repository:** [https://github.com/ishaan-gitoutlook/Stock_Tracker_App](https://github.com/ishaan-gitoutlook/Stock_Tracker_App)
- **Developed by:** Ishaan
