# 📈 Stock Tracker App

[![CI/CD Pipeline](https://github.com/ishaan-gitoutlook/Stock_Tracker_App/actions/workflows/ci.yml/badge.svg)](https://github.com/ishaan-gitoutlook/Stock_Tracker_App/actions/workflows/ci.yml)
[![CI: Jenkins](https://img.shields.io/badge/CI%2FCD-Jenkins%20Pipeline-D24939.svg?logo=jenkins&logoColor=white)](Jenkinsfile)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](Dockerfile)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/Tests-41%20Passing-brightgreen.svg)](tests/)
[![AI Assistant](https://img.shields.io/badge/AI%20Assistant-Gemini%20%7C%20Ollama%20%7C%20Heuristic-purple.svg)]()
[![Architecture](https://img.shields.io/badge/Architecture-2--Tier%20Microservice-orange.svg)]()
[![License](https://img.shields.io/badge/License-Educational%20Use-lightgrey.svg)]()

A modern, full-stack financial tracking dashboard and REST API built for educational purposes. The platform combines **FastAPI** for application APIs, a separate normalized **market-data service** for end-of-day ingestion, and **Streamlit** for reactive data visualization, with fallback quotes, an AI assistant, and an interactive terminal CLI.

---

## 📑 Table of Contents

- [System Architecture](#-system-architecture)
- [✨ Key Features](#-key-features)
- [🤖 Free AI Financial Assistant](#-free-ai-financial-assistant)
- [📁 Project Structure](#-project-structure)
- [🌐 REST API Reference](#-rest-api-reference)
- [🚀 Quick Start (Local Setup)](#-quick-start-local-setup)
- [🧪 Running Automated Tests](#-running-automated-tests)
- [🔧 Troubleshooting & Common Issues](#-troubleshooting--common-issues)
- [⚙️ CI/CD Automation (GitHub Actions & Jenkins)](#️-cicd-automation-github-actions--jenkins)
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

## 🗄️ Custom Market-Data Service

The repository now includes a separate normalized end-of-day market-data service under `src/market_data/`. It is designed to ingest licensed exchange/vendor data, preserve immutable source payloads, normalize listings and daily prices, and serve the dashboard through a versioned internal API.

Initial exchange scope:

- India: NSE and BSE
- United States: NYSE and Nasdaq
- Europe: LSE and Xetra

The development connector uses EODHD. Production deployments should replace it with licensed exchange or authorized vendor connectors before redistributing data. The service stores normalized data in PostgreSQL in production and uses SQLite by default for local development. It currently supports listing synchronization and daily-price ingestion; fundamentals and corporate-action storage endpoints return explicit unavailable states until their ingestion connectors are configured.

### Market-data service commands

```bash
# Run the private API locally with SQLite
uvicorn src.market_data.api:app --reload --port 8001

# Seed development exchange listings
python -m src.market_data.worker listings NSE
python -m src.market_data.worker listings BSE
```

For PostgreSQL and the service container stack:

```bash
docker compose -f docker-compose.market-data.yml up -d market-data-db market-data-api
docker compose -f docker-compose.market-data.yml --profile worker run --rm market-data-worker
```

The market-data API is protected with `MARKET_DATA_API_TOKEN` when configured. The Streamlit app can consume it by setting `MARKET_DATA_API_URL` and the same token in its deployment secrets.

---

## ✨ Key Features

### 📊 Reactive Frontend (Streamlit)
- **Rebuilt Market Desk UI:** A responsive HTML/CSS presentation layer with a workspace header, active-universe context card, live-feed status pill, polished tabs, responsive layouts, and elevated data surfaces.
- **Design System:** Theme-aware CSS variables, typography, cards, tables, controls, metric states, hover treatments, and mobile breakpoints are generated from `src/themes.py`.
- **Live Price Updates:** Real-time stock ticker quotes refreshed every 5 seconds using non-blocking Streamlit fragments (`@st.fragment`).
- **Interactive Metric Cards:** Displays company name, current market price, and colored price movement deltas ($\Delta$ with absolute value and percentage).
- **Light & Dark Theme Modes:** Built-in theme selector with high-contrast color systems tailored for day and night viewing.
- **Floating AI Assistant Launcher:** Bottom-right floating trigger button (`💬 AI`) with smooth CSS pulse animation for instant drawer-based chat without page clutter.
- **Hero Status Banner:** Gradient header panel with live ticker counter and real-time connection status dot (`● LIVE`).
- **Curated Market Universes:** Filter and track major stock collections, including **NIFTY 500**, **Fortune 500**, and personal watchlists.
- **Dynamic Ticker Adder:** Search and add any valid global ticker symbol (e.g., `NVDA`, `TSLA`, `RELIANCE.NS`, `BTC-USD`) on the fly with automatic deduplication.
- **Comprehensive Market Table:** Detailed overview containing daily price range ($Low - High$), 24-hour volume, and net change.
- **Instant Manual Refresh:** Clear the UI cache on demand with a single click.

The dashboard opens with the **Market Desk** workspace header, then separates the experience into two focused views:

1. **Live market** — listing selection, tracked-stock metric cards, intraday comparison, market overview table, CSV export, and the AI copilot.
2. **Fundamentals research** — searchable India, United States, and Europe research workspaces with watchlists, history, valuation, profitability, statements, dividends, and company details.

The UI remains fully Streamlit-native: HTML and CSS improve the visual layer while Streamlit widgets continue to provide accessible interaction, state management, and server-side rendering.

### ⚡ Asynchronous REST API (FastAPI)
- **Interactive Documentation:** Automated Swagger UI (`/docs`) and ReDoc (`/redoc`) exploring data contracts and schemas.
- **High Concurrency:** Utilizes Python's `concurrent.futures.ThreadPoolExecutor` to fetch multiple symbols simultaneously in $<0.8\text{s}$.
- **Health Checks:** Built-in `/health` probe for automated container and service monitoring.

### 💻 Command-Line Interface (CLI)
- **Terminal Price Ticker:** Lightweight console view with formatted ASCII tables and auto-clearing screens for terminal enthusiasts.

### 🤖 Free AI Financial Assistant
- **Dual Cloud & Local Execution:** Seamlessly switches between **Google Gemini Flash (Free Cloud Tier)** and **Ollama (100% Offline Local LLM)**.
- **Context-Aware Reasoning:** Injects the live prices, deltas, volumes, and daily ranges of currently selected stocks directly into the model's prompt.
- **Offline Heuristic Fallback:** If no API key or Ollama daemon is running, a built-in financial rule engine answers questions (top gainers, losers, highest volume, price comparisons) with zero external dependencies.
- **Interactive UI with Quick Prompts:** Single-click prompt chips (`📈 Top Gainer Today?`, `📉 Biggest Decline?`, `📊 Portfolio Summary`) and live chat interface.

---

## 🤖 Free AI Financial Assistant

The assistant operates with **zero mandatory setup** through a 3-tier resolution hierarchy:

```
                  User Query
                      │
                      ▼
         [ Live Market Context Injection ]
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
     [ Gemini ]   [ Ollama ]   [ Heuristic ]
    (Free Cloud)   (Local)      (Offline)
```

### Supported Provider Options:

The assistant is restricted to tracked-stock and stock-performance questions. Out-of-scope questions receive `I don't know.` It does not issue buy/sell recommendations, and comparison or investment-related questions include a risk disclaimer. Provider output is capped at 10,000 tokens per query.

1. **Option 1: Google Gemini (Free Cloud Tier — Recommended for Streamlit Cloud)**
   - Get a free API key from [Google AI Studio](https://aistudio.google.com/) (No credit card needed).
   - Locally: add `GEMINI_API_KEY="your-key"` to your `.env` or environment.
   - Streamlit Cloud: add `GEMINI_API_KEY = "your-key"` to your app's **Secrets** settings.
   - Teachers and friends opening your public link can chat with the assistant 24/7!

2. **Option 2: Local Ollama (100% Offline & Private)**
   - Install [Ollama](https://ollama.ai) and pull any model (e.g. `llama3.2:3b` or `tinyllama`):
     ```bash
     ollama run tinyllama
     ```
   - The app automatically detects Ollama running at `http://127.0.0.1:11434` and uses it locally with zero internet.

3. **Option 3: Built-in Heuristic Analyst (Zero-Configuration Fallback)**
   - If neither a Gemini key nor Ollama is configured, the built-in financial rule engine automatically takes over, answering questions about gainers, losers, price spreads, and volume rankings without any errors.

---

## 📁 Project Structure

```text
Stock_Tracker_App/
│
├── src/                                  # Modular application source code
│   ├── __init__.py                       # Package initializer
│   ├── tracker.py                        # Core domain models & parallel data fetcher
│   ├── universes.py                      # Curated market indices and listing presets
│   ├── assistant.py                      # Free LLM & heuristic financial assistant engine
│   ├── api.py                            # FastAPI REST service & route definitions
│   ├── api_client.py                     # Resilient HTTP client with secret resolution
│   ├── themes.py                         # Design tokens, color palettes & responsive CSS
│   ├── dashboard.py                      # Market Desk UI, metrics, listings & AI chat
│   └── market_data/                      # Normalized EOD provider, storage, API & workers
│
├── tests/                                # Automated unit test suite (41 tests)
│   ├── __init__.py                       # Test package initializer
│   ├── test_tracker.py                   # Data parsing, calculations & fallback tests
│   ├── test_assistant.py                 # AI prompt generation, provider & heuristic tests
│   ├── test_chat_api.py                  # FastAPI chat endpoint & client wrapper tests
│   ├── test_api_client.py                # HTTP client serialization & error handling tests
│   └── test_dashboard.py                 # Universe indexing, fallback mode & theme tests
│
├── .github/                              # CI/CD automation workflows
│   └── workflows/ci.yml                  # GitHub Actions test and quality pipeline
├── Jenkinsfile                           # Declarative Jenkins CI/CD pipeline
├── Dockerfile                            # Main application container definition
├── docker-compose.market-data.yml        # PostgreSQL + market-data API/worker stack
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
| `POST` | `/api/v1/chat` | AI Assistant answering queries with live market context | `{"message": "Top gainer?", "symbols": ["AAPL"]}` |

### Normalized market-data API

Run the separate service on `http://127.0.0.1:8001` to use these versioned endpoints:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/v1/health` | Market-data service health |
| `GET` | `/v1/markets` | Supported market groups |
| `GET` | `/v1/exchanges` | Core exchange metadata |
| `GET` | `/v1/instruments/search?q=...` | Search normalized instruments |
| `GET` | `/v1/exchanges/{exchange}/listings` | Paginated active exchange listings |
| `GET` | `/v1/instruments/{id}` | Instrument metadata |
| `GET` | `/v1/instruments/{id}/prices` | Normalized daily OHLCV history |
| `GET` | `/v1/instruments/{id}/fundamentals` | Fundamental metrics or unavailable status |
| `GET` | `/v1/instruments/{id}/corporate-actions` | Corporate actions or unavailable status |
| `GET` | `/v1/ingestion/runs` | Ingestion history and failures |

When `MARKET_DATA_API_TOKEN` is set, send it as the `X-Market-Data-Token` header.

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
.\.venv\Scripts\Activate.ps1

# Note for Windows: If script execution is restricted in PowerShell, run:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# Or run without activation: .\.venv\Scripts\python.exe -m streamlit run main.py

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

#### Mode A2: Normalized Market-Data Service

Run the application API and normalized market-data API separately when testing the custom provider:

```bash
# Terminal 1: application API
uvicorn src.api:app --reload --port 8000

# Terminal 2: market-data API
uvicorn src.market_data.api:app --reload --port 8001

# Terminal 3: Streamlit dashboard
# PowerShell: $env:MARKET_DATA_API_URL="http://127.0.0.1:8001"
# PowerShell: $env:MARKET_DATA_API_TOKEN="local-market-data-token"
streamlit run main.py
```

The market-data API defaults to SQLite. Set `DATABASE_URL` to a PostgreSQL URL for a deployed instance.

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

To run an individual test file:
```bash
# Directly as a script:
python tests/test_api_client.py

# Or via unittest module:
python -m unittest tests/test_api_client.py
```

Expected output (the exact duration can vary by machine):
```text
.........................................
----------------------------------------------------------------------
Ran 41 tests in ...s

OK
```

---

## 🔧 Troubleshooting & Common Issues

### 1. `'streamlit' is not recognized as an internal or external command` (or exits with code 1)
- **Cause:** The virtual environment has not been activated in your current terminal session, or `streamlit` is not on the system PATH.
- **Solution:** Activate your virtual environment in PowerShell:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  streamlit run main.py
  ```
  Or run Streamlit directly via the virtual environment interpreter without needing activation:
  ```powershell
  .\.venv\Scripts\python.exe -m streamlit run main.py
  ```

### 2. `Port 8501 is not available`
- **Cause:** Another Streamlit process or background service is already listening on default port `8501`.
- **Solution:** Stop the existing process:
  ```powershell
  # Check and stop process using port 8501 (PowerShell)
  $conn = Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue
  if ($conn) { Stop-Process -Id $conn.OwningProcess -Force }
  ```
  Or launch Streamlit on an alternative port:
  ```bash
  streamlit run main.py --server.port 8502
  ```

### 3. Relocated Virtual Environment (Silent Exit Code 1)
- **Cause:** If the project directory was moved, renamed, or copied, Windows console executable wrappers in `.venv/Scripts/` (e.g., `streamlit.exe`, `uvicorn.exe`, `pip.exe`) can retain outdated hardcoded interpreter paths, causing them to fail immediately upon invocation.
- **Solution:** Reinstall the console script wrappers to point to the current environment:
  ```powershell
  .\.venv\Scripts\python.exe -m pip install --force-reinstall --no-deps streamlit uvicorn pip
  ```

---

## ⚙️ CI/CD Automation (GitHub Actions & Jenkins)

The project includes continuous integration and automated quality pipelines through two enterprise-grade CI/CD setups:

### 1. GitHub Actions (`.github/workflows/ci.yml`)
- **Automated Trigger:** Executes automatically on every `git push` or `pull_request` to the `master` branch.
- **Matrix Testing:** Validates the test suite concurrently across **Python 3.11** and **Python 3.12**.
- **Pipeline Workflow:**
  1. Dependency installation from `requirements.txt` with pip caching.
  2. Execution of the complete 41-test unit suite (`python -m unittest discover tests`).
  3. Integrity smoke test ensuring both FastAPI and Streamlit modules import cleanly.

### 2. Jenkins Pipeline (`Jenkinsfile`)
For teams utilizing Jenkins automation servers:
- **Declarative Pipeline:** Contains isolated stages for `Checkout`, `Setup Environment`, `Unit Tests`, `Smoke Test`, and `Deploy Notification`.
- **Clean Workspace:** Automatically generates and tears down a disposable virtual environment (`.venv-ci`) for each run.
- **Docker Support (`Dockerfile`):** Ready to be built and executed inside containerized Jenkins agents or Kubernetes pods.

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

For the normalized provider, add these values under the app's **Settings → Secrets**:

```toml
MARKET_DATA_API_URL = "https://your-market-data-api.example.com"
MARKET_DATA_API_TOKEN = "your-internal-service-token"
EODHD_API_KEY = "your-development-or-licensed-provider-key"
```

Do not commit secrets or licensed raw market data to GitHub.

### 3. Standalone Mode (Zero-Config)
If you deploy only Streamlit without configuring `MARKET_DATA_API_URL` or `EODHD_API_KEY`, the dashboard can still show its small curated Yahoo fallback lists. Complete exchange catalogs and normalized provider data require the market-data service and credentials.

---

## ⚙️ Configuration & Environment Variables

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `STOCK_API_URL` | `http://127.0.0.1:8000` | Base endpoint of the FastAPI backend. Can also be defined in Streamlit Cloud Secrets. |
| `MARKET_DATA_API_URL` | unset | Private normalized market-data API used by the dashboard. |
| `MARKET_DATA_API_TOKEN` | unset | Shared token for the private market-data API. |
| `DATABASE_URL` | `sqlite:///./market_data.db` | PostgreSQL URL for production market-data storage; SQLite is the local default. |
| `EODHD_API_KEY` | unset | Development source credential for EODHD listing/history ingestion. |
| `MARKET_DATA_RAW_DIR` | `./market_data_raw` | Local raw payload archive directory for development ingestion. |
| `REFRESH_SECONDS`| `5` | Polling interval for live stock quote refreshes. |
| `REQUEST_TIMEOUT`| `8` | Network timeout in seconds for upstream financial queries. |

---

## 📄 Educational Disclaimer

This project was developed strictly for **educational and demonstration purposes**. Market data is fetched from publicly available endpoints. It is not intended for live automated trading or investment advisory services.

---

## 👨‍💻 Author & Repository

- **Repository:** [https://github.com/ishaan-gitoutlook/Stock_Tracker_App](https://github.com/ishaan-gitoutlook/Stock_Tracker_App)
- **Developed by:** Ishaan
