# 📈 StockPulse — Enterprise Financial Intelligence & AI QA Platform

[![CI/CD Pipeline](https://github.com/ishaan-gitoutlook/Stock_Tracker_App/actions/workflows/ci.yml/badge.svg)](https://github.com/ishaan-gitoutlook/Stock_Tracker_App/actions/workflows/ci.yml)
[![CI: Jenkins](https://img.shields.io/badge/CI%2FCD-Jenkins%20Pipeline-D24939.svg?logo=jenkins&logoColor=white)](Jenkinsfile)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](Dockerfile)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-v1.63%2B-45ba4b.svg?logo=playwright&logoColor=white)](https://playwright.dev/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-orange.svg)]()
[![AI QA Suite](https://img.shields.io/badge/AI%20QA-Nemotron%20%7C%20Ollama-purple.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-Educational%20Use-lightgrey.svg)]()

**StockPulse** is a modern, production-grade financial tracking ecosystem, market intelligence dashboard, and autonomous QA testing platform. It combines a resilient **FastAPI** backend, a normalized **EOD market-data service**, an interactive **Streamlit** multi-market dashboard, an **AI Copilot** (Gemini / Ollama), and a cutting-edge **Autonomous AI QA Test Suite** powered by **Playwright** and the **Model Context Protocol (MCP)**.

---

## 📑 Table of Contents

- [🏛️ System Architecture](#️-system-architecture)
- [✨ Key Capabilities](#-key-capabilities)
  - [1. Multi-Market Watchlists & Universes](#1-multi-market-watchlists--universes)
  - [2. Dual-Tab Intelligence (Quotes & Fundamentals)](#2-dual-tab-intelligence-quotes--fundamentals)
  - [3. 7 Ergonomic Theme Palettes](#3-7-ergonomic-theme-palettes)
  - [4. AI Financial Copilot](#4-ai-financial-copilot)
- [🤖 3-Tier Testing & QA Suite](#-3-tier-testing--qa-suite)
  - [Layer 1: Python Unit & Integration Tests](#layer-1-python-unit--integration-tests)
  - [Layer 2: Playwright End-to-End Tests](#layer-2-playwright-end-to-end-tests)
  - [Layer 3: Autonomous AI QA Suite (MCP + Ollama)](#layer-3-autonomous-ai-qa-suite-mcp--ollama)
- [📁 Repository Structure](#-repository-structure)
- [🚀 Quick Start (Local Setup)](#-quick-start-local-setup)
- [🐳 Docker & Compose Deployment](#-docker--compose-deployment)
- [🌐 REST API Reference](#-rest-api-reference)
- [⚙️ Configuration & Environment Variables](#️-configuration--environment-variables)
- [🔧 Troubleshooting & FAQ](#-troubleshooting--faq)
- [📄 Educational Disclaimer](#-educational-disclaimer)

---

## 🏛️ System Architecture

StockPulse is designed around an enterprise microservices pattern with built-in failover:

```
┌────────────────────────────────────────────────────────────────────────┐
│                         CLIENT INTERFACES                              │
│                                                                        │
│   Streamlit Web UI (main.py)           Terminal CLI (cli.py)           │
│   - Multi-Market Radar                 - Live ASCII ticker table       │
│   - Fundamentals Research              - Instant console quotes        │
│   - 7 Ergonomic Color Themes                                           │
└───────────────────┬───────────────────────────────┬────────────────────┘
                    │                               │
         HTTP / REST│ (APIClient with Fallback)     │ Direct Fallback
                    ▼                               ▼
┌────────────────────────────────────────┐  ┌────────────────────────────┐
│          CORE FASTAPI BACKEND          │  │       YAHOO FINANCE        │
│          (src/api.py :8000)            │  │      UPSTREAM / DIRECT     │
│   - /api/v1/quotes                     │  │      (src/tracker.py)      │
│   - /api/v1/universes                  │  └─────────────▲──────────────┘
│   - /api/v1/chat (AI Assistant)        │                │
│   - /health                            │                │
└───────────────────┬────────────────────┘                │
                    │                                     │
         HTTP / REST│                                     │
                    ▼                                     │
┌────────────────────────────────────────┐                │
│       MARKET DATA SERVICE (EOD)        │                │
│       (src/market_data/ :8001)         │                │
│   - Normalized Exchange Storage        │────────────────┘
│   - PostgreSQL 16 / SQLite             │
│   - Scheduled Ingestion Workers        │
└────────────────────────────────────────┘

══════════════════════════════════════════════════════════════════════════
               AUTONOMOUS AI QA AUTOMATION LAYER
══════════════════════════════════════════════════════════════════════════
┌──────────────────────┐      MCP JSON-RPC      ┌────────────────────────┐
│  OLLAMA AI ENGINE    │◄──────────────────────►│  PLAYWRIGHT MCP SERVER │
│ (nemotron-3-super)   │   (Tools & ARIA Tree)  │   (@playwright/mcp)    │
└──────────┬───────────┘                        └───────────┬────────────┘
           │                                                │
           │ Evaluates Pass/Fail                            │ Drives Browser
           ▼                                                ▼
┌──────────────────────┐                        ┌────────────────────────┐
│ Markdown Test Report │                        │ Chromium Headed/Headless│
│  & PNG Evidence      │                        │ (http://localhost:8501)│
└──────────────────────┘                        └────────────────────────┘
```

---

## ✨ Key Capabilities

### 1. Multi-Market Watchlists & Universes
Track blue-chip indices and global megacaps out of the box:
* 🇮🇳 **NIFTY 500 & BSE Sensex 30** (National Stock Exchange & Bombay Stock Exchange)
* 🇺🇸 **S&P 500 / Fortune 500 & NASDAQ 100** (US Large Cap & Tech Leaders)
* 🇬🇧 **FTSE 100** (London Stock Exchange)
* 🇩🇪 **DAX 40** (Deutsche Börse XETRA)
* 🌐 **Global Megacaps** (Apple, Microsoft, Alphabet, Nvidia, Reliance, etc.)
* ⭐ **Custom User Watchlists** (Input any global ticker symbol)

### 2. Dual-Tab Intelligence (Quotes & Fundamentals)
* **Live Market Tracker & Listings**: Intraday momentum, daily breadth ratios, visual performance charts, and auto-syncing financial quotes.
* **In-Depth Fundamentals Research**: Valuation ratios, P/E, EPS, market capitalization, balance sheet stability, and exchange mappings.

### 3. 7 Ergonomic Theme Palettes
Customize the dashboard aesthetic instantly with zero page reloads:
* 🌙 **Midnight Navy** (Ergonomic Dark)
* ☀️ **Clean Light** (Glare-Free Paper)
* 🖤 **Obsidian Noir** (OLED High-Contrast)
* 🌲 **Emerald Wealth** (Calm Forest Green)
* ❄️ **Arctic Frost** (Nordic Minimalist Mist)
* 🌇 **Crimson Sunset** (Warm Twilight Ember)
* 💻 **Solarized Dark** (Developer Classic)

### 4. AI Financial Copilot
* Supports **Google Gemini API** (`gemini-1.5-flash`), local/cloud **Ollama** (`nemotron-3-super:cloud`, `llama3.2`, `qwen2.5`), or built-in **Rule-Based Heuristics**.
* Financial domain guardrails, question scope validation, and mandatory risk disclaimers.

---

## 🤖 3-Tier Testing & QA Suite

StockPulse features a complete, multi-layered quality assurance architecture:

```
┌────────────────────────────────────────────────────────────────────────┐
│ Level 3: Autonomous AI QA Suite (Playwright + MCP + Ollama)            │
│          - Natural language YAML scenarios evaluated by AI Agent       │
│          - Reads accessibility ARIA tree, outputs pass/fail reports    │
├────────────────────────────────────────────────────────────────────────┤
│ Level 2: Playwright End-to-End UI Tests (TypeScript/Node.js)           │
│          - 16 interactive tests verifying UI rendering, selectors,     │
│            sidebar dynamics, and Streamlit state changes               │
├────────────────────────────────────────────────────────────────────────┤
│ Level 1: Python Unit & Integration Tests (Python unittest)             │
│          - 41 tests verifying calculations, REST APIs, and fallbacks   │
└────────────────────────────────────────────────────────────────────────┘
```

### Layer 1: Python Unit & Integration Tests
Runs all 41 test cases across the API client, assistant, chat, and market data modules:
```bash
python -m unittest discover tests
```

### Layer 2: Playwright End-to-End Tests
Visual and interactive tests running against the real browser:
```bash
# Run headlessly in the background
npm run test:e2e

# Run with visible browser window to watch interactions
npm run test:e2e:headed
```

**Test Specifications (`tests/e2e/`):**
* `01-hello-world.spec.ts`: Page navigation, title verification, and search inputs.
* `02-locators.spec.ts`: Accessibility-first locators (`getByRole`, `getByPlaceholder`, chaining).
* `03-stock-dashboard.spec.ts`: Live testing of StockPulse sidebar, presets, branding, and ARIA tree.
* `04-mcp-simulation.spec.ts`: MCP ARIA snapshot inspection and See→Think→Act loop simulation.

### Layer 3: Autonomous AI QA Suite (MCP + Ollama)
A fully autonomous AI test runner that reads declarative plain-English test scenarios from YAML, drives Chromium via Playwright, and issues verdicts:

```bash
# Start your application first in one terminal:
streamlit run main.py

# In a second terminal, execute the AI QA suite:
npm run test:ai
```

* **Test Scenarios (`tests/ai_agent/test_scenarios.yaml`)**: Declarative test definitions.
* **Test Runner (`tests/ai_agent/runner.py`)**: Connects to `nemotron-3-super:cloud` (or any Ollama/cloud model), uses Playwright MCP tools, captures screenshots, and generates reports.
* **Automated Report (`tests/ai_agent/reports/test_report.md`)**: Complete summary with pass/fail badges, model rationale, and screenshot evidence (**100% PASS**).

---

## 📁 Repository Structure

```
Stock_Tracker_App/
├── src/                               # Application source code
│   ├── api.py                         # FastAPI REST application
│   ├── api_client.py                  # API client with automatic offline fallback
│   ├── assistant.py                   # AI Financial Copilot (Gemini/Ollama/Heuristics)
│   ├── dashboard.py                   # Streamlit web dashboard
│   ├── research.py                    # Fundamentals research data adapter
│   ├── research_ui.py                 # Fundamentals UI tab renderer
│   ├── themes.py                      # 7 ergonomic UI color palettes
│   ├── tracker.py                     # Stock quote fetching & caching engine
│   ├── universes.py                   # Global market listings & index constituents
│   └── market_data/                   # Normalized EOD market-data microservice
│       ├── api.py                     # Market-data FastAPI service
│       ├── ingest.py                  # Exchange catalog ingestion pipeline
│       ├── models.py                  # SQLAlchemy domain entities
│       ├── normalization.py           # Symbology and price normalization
│       ├── storage.py                 # PostgreSQL & SQLite repository layer
│       └── worker.py                  # CLI catalog worker
├── tests/                             # Comprehensive test suites
│   ├── test_api_client.py             # Client unit tests
│   ├── test_assistant.py              # AI assistant guardrail tests
│   ├── test_chat_api.py               # Chat endpoint tests
│   ├── test_dashboard.py              # Streamlit state tests
│   ├── test_market_data.py            # Ingestion & storage tests
│   ├── test_tracker.py                # Quote calculation tests
│   ├── e2e/                           # Layer 2: Playwright E2E tests
│   │   ├── 01-hello-world.spec.ts     # Basic navigation & assertions
│   │   ├── 02-locators.spec.ts        # Role-based locator tests
│   │   ├── 03-stock-dashboard.spec.ts # Streamlit dashboard test suite (7/7 passed)
│   │   ├── 04-mcp-simulation.spec.ts  # MCP ARIA simulation (3/3 passed)
│   │   └── screenshots/               # Baseline visual snapshots
│   └── ai_agent/                      # Layer 3: Autonomous AI QA suite
│       ├── agent.py                   # Interactive AI browser agent
│       ├── runner.py                  # YAML-driven test runner
│       ├── test_scenarios.yaml        # Natural language test cases
│       └── reports/                   # Generated reports & PNG evidence
│           ├── test_report.md         # 100% Pass Execution Report
│           └── screenshot_*.png       # Visual test evidence
├── .github/workflows/ci.yml           # GitHub Actions automated CI workflow
├── .vscode/mcp.json                   # Playwright MCP server registration
├── playwright.config.ts               # Playwright test configuration
├── package.json                       # Node.js test scripts & dependencies
├── Dockerfile                         # Production multi-stage Docker build
├── docker-compose.market-data.yml     # PostgreSQL + Market-Data compose stack
├── Jenkinsfile                        # Declarative Jenkins CI/CD pipeline
├── main.py                            # Streamlit application entrypoint
├── cli.py                             # Interactive terminal CLI tracker
├── requirements.txt                   # Python dependencies
└── WALKTHROUGH.md                     # Complete project walkthrough guide
```

---

## 🚀 Quick Start (Local Setup)

### 1. Clone & Setup Python Environment

```powershell
# Clone repository
git clone https://github.com/ishaan-gitoutlook/Stock_Tracker_App.git
cd Stock_Tracker_App

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Install Playwright & Node.js Dependencies

```powershell
# Install npm dependencies
npm install

# Install Playwright browser binaries
npx playwright install chromium
```

### 3. Run the Application

You can launch StockPulse in three distinct modes:

#### Option A: Standalone Dashboard (Easiest)
```powershell
streamlit run main.py
```
*Opens automatically at `http://localhost:8501`. Automatically falls back to direct financial fetching with zero external services required.*

#### Option B: Full Microservices Stack
```powershell
# Terminal 1: Core API Backend
uvicorn src.api:app --reload --port 8000

# Terminal 2: Streamlit Frontend
streamlit run main.py
```

#### Option C: Terminal CLI Tracker
```powershell
python cli.py
```

---

## 🐳 Docker & Compose Deployment

Run the complete isolated stack with PostgreSQL:

```bash
# Build and run the Market-Data Service + PostgreSQL 16
docker compose -f docker-compose.market-data.yml up -d

# Build and run the Web Dashboard
docker build -t stockpulse .
docker run -p 8501:8501 stockpulse
```

---

## 🌐 REST API Reference

| Method | Endpoint | Description |
|:---|:---|:---|
| `GET` | `/health` | Service health status and uptime |
| `GET` | `/api/v1/quotes?symbols=AAPL,MSFT` | Fetch real-time quotes, price changes, and breadth |
| `GET` | `/api/v1/universes` | List all available market listings (NIFTY, S&P, NASDAQ, etc.) |
| `POST` | `/api/v1/chat` | Query the AI financial copilot with tracked market context |

---

## ⚙️ Configuration & Environment Variables

| Variable | Default | Purpose |
|:---|:---|:---|
| `STOCK_API_URL` | `http://127.0.0.1:8000` | URL for the core FastAPI backend |
| `MARKET_DATA_API_URL` | `http://127.0.0.1:8001` | URL for the normalized market data service |
| `MARKET_DATA_API_TOKEN` | `local-market-data-token` | Authorization token for market data endpoints |
| `DATABASE_URL` | `sqlite:///./market_data.db` | Storage backend (supports SQLite & PostgreSQL) |
| `GEMINI_API_KEY` | *(None)* | Google AI Studio key for cloud Gemini Copilot |
| `OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | Endpoint for local or cloud Ollama instance |
| `OLLAMA_MODEL` | `nemotron-3-super:cloud` | Default model for autonomous QA testing |

---

## 🔧 Troubleshooting & FAQ

### 1. `Port 8501 is already in use`
A previous Streamlit process is still listening. Kill it via PowerShell:
```powershell
$conn = Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue
if ($conn) { Stop-Process -Id $conn.OwningProcess -Force }
```

### 2. `Playwright certificate error on download`
If running on a protected network:
```powershell
$env:NODE_TLS_REJECT_UNAUTHORIZED="0"
npx playwright install chromium
```

### 3. `How to run tests without Ollama?`
You can always run the Playwright E2E suite (`npm run test:e2e`) and Python unit tests (`python -m unittest discover tests`), which require no LLM at all.

---

## 📄 Educational Disclaimer

*StockPulse is developed exclusively for educational and demonstration purposes. Financial market data is subject to exchange delays. The built-in AI Copilot does not constitute registered financial, investment, or legal advice. Always conduct your own research before trading.*
