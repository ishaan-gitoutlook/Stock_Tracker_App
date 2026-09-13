"""FastAPI backend for stock quotes and market universes."""

from dataclasses import asdict
from typing import List, Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

from src.tracker import DEFAULT_SYMBOLS, get_prices
from src.universes import MARKET_UNIVERSES


class QuoteResponse(BaseModel):
    """JSON representation of one quote returned by the API."""

    symbol: str
    name: str
    price: float
    currency: str
    previous_close: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    day_high: Optional[float] = None
    day_low: Optional[float] = None
    volume: Optional[int] = None


class QuotesResponse(BaseModel):
    """Response envelope for a quote request."""

    quotes: List[QuoteResponse]
    requested_symbols: List[str]
    missing_symbols: List[str]


class UniverseResponse(BaseModel):
    """A named set of ticker symbols available to the frontend."""

    name: str
    symbols: List[str]


class ChatRequest(BaseModel):
    """Request payload for the AI financial assistant."""

    message: str
    symbols: Optional[List[str]] = None
    ollama_model: Optional[str] = None


class ChatResponse(BaseModel):
    """Response returned by the AI financial assistant."""

    reply: str
    provider: str
    symbols_used: List[str]


app = FastAPI(
    title="Stock Tracker API",
    version="1.1.0",
    description="Quote, market-universe, and AI Financial Assistant service for the Streamlit dashboard.",
)


def parse_symbols(symbols: Optional[str]) -> List[str]:
    """Normalize a comma-separated symbol query while preserving order."""
    raw_symbols = symbols.split(",") if symbols else list(DEFAULT_SYMBOLS)
    return list(dict.fromkeys(symbol.strip().upper() for symbol in raw_symbols if symbol.strip()))


@app.get("/health")
def health() -> dict:
    """Return a lightweight service health response."""
    return {"status": "ok"}


@app.get("/")
def root() -> dict:
    """Provide a discoverable landing response for the deployed API."""
    return {
        "service": "Stock Tracker API",
        "status": "ok",
        "docs": "/docs",
        "health": "/health",
        "quotes": "/api/v1/quotes",
        "universes": "/api/v1/universes",
        "chat": "/api/v1/chat",
    }


@app.get("/api/v1/universes", response_model=List[UniverseResponse])
def list_universes() -> List[UniverseResponse]:
    """List the curated ticker universes available to the dashboard."""
    return [UniverseResponse(name=name, symbols=list(symbols)) for name, symbols in MARKET_UNIVERSES.items()]


@app.get("/api/v1/quotes", response_model=QuotesResponse)
def list_quotes(
    symbols: Optional[str] = Query(
        default=None,
        description="Comma-separated Yahoo Finance ticker symbols.",
    ),
    fresh: bool = Query(
        default=False,
        description="Reserved for clients that explicitly request a fresh fetch.",
    ),
) -> QuotesResponse:
    """Fetch the latest quotes for the requested symbols concurrently."""
    del fresh  # The backend fetcher is uncached; each request is already fresh.
    requested_symbols = parse_symbols(symbols)
    quote_map = get_prices(requested_symbols)
    quotes = [QuoteResponse(**asdict(quote)) for quote in quote_map.values()]
    missing_symbols = [symbol for symbol in requested_symbols if symbol not in quote_map]
    return QuotesResponse(
        quotes=quotes,
        requested_symbols=requested_symbols,
        missing_symbols=missing_symbols,
    )


@app.post("/api/v1/chat", response_model=ChatResponse)
def chat_assistant(request: ChatRequest) -> ChatResponse:
    """Answer market queries using live stock data and AI/heuristic engines."""
    from src.assistant import ask_assistant

    symbols = [s.strip().upper() for s in (request.symbols or []) if s.strip()]
    quotes = get_prices(symbols) if symbols else {}
    reply, provider = ask_assistant(
        question=request.message,
        quotes=quotes,
        ollama_model=request.ollama_model,
    )
    return ChatResponse(
        reply=reply,
        provider=provider,
        symbols_used=list(quotes.keys()),
    )
