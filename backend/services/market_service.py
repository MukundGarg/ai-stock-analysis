"""
Market Service Module

Fetches stock quotes, candlestick data, and market news from Finnhub API.
"""

import os
import httpx
from typing import Any, Optional
from datetime import datetime, timedelta, timezone


async def get_stock_quote(symbol: str) -> dict:
    """
    Fetch latest stock price using Finnhub /quote endpoint.

    Args:
        symbol: Stock symbol (e.g., "AAPL", "TSLA", "RELIANCE.NS")

    Returns:
        Dict with fields: symbol, current_price, change, change_percent, 
                        high, low, open, previous_close, timestamp

    Raises:
        ValueError: If API key is missing or symbol is invalid
    """
    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        raise ValueError(
            "FINNHUB_API_KEY environment variable not set. "
            "Please set your Finnhub API key from https://finnhub.io"
        )

    if not symbol or len(symbol.strip()) == 0:
        raise ValueError("Symbol cannot be empty")

    symbol = symbol.strip().upper()
    if len(symbol) > 20:
        raise ValueError("Symbol cannot be longer than 20 characters")

    endpoint = "https://finnhub.io/api/v1/quote"
    params = {
        "symbol": symbol,
        "token": api_key,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            # Check if API returned an error
            if "error" in data:
                raise ValueError(f"Finnhub API error: {data['error']}")

            # Check if valid data returned
            if data.get("c") is None:
                raise ValueError(f"Invalid symbol or no data available for {symbol}")

            # Format response
            formatted = {
                "symbol": symbol,
                "current_price": data.get("c", 0),
                "change": data.get("d", 0),
                "change_percent": data.get("dp", 0),
                "high": data.get("h", 0),
                "low": data.get("l", 0),
                "open": data.get("o", 0),
                "previous_close": data.get("pc", 0),
                "timestamp": data.get("t", 0),
            }

            return formatted

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Finnhub API authentication failed. Check your API key.")
        elif e.response.status_code == 429:
            raise ValueError("Finnhub API rate limit exceeded. Try again later.")
        else:
            raise ValueError(f"Finnhub API request failed: {str(e)}")

    except httpx.RequestError as e:
        raise ValueError(f"Failed to connect to Finnhub API: {str(e)}")

    except Exception as e:
        raise ValueError(f"Error fetching stock quote: {str(e)}")


async def get_stock_candles(
    symbol: str,
    resolution: str = "D",
    count: int = 30,
) -> dict:
    """
    Fetch OHLC candlestick data using Finnhub /stock/candle endpoint.

    Args:
        symbol: Stock symbol (e.g., "AAPL", "TSLA", "RELIANCE.NS")
        resolution: Time resolution (1, 5, 15, 30, 60, D, W, M)
        count: Number of candles to fetch (default 30)

    Returns:
        Dict with fields: symbol, resolution, candles (list of dicts with
                        timestamp, open, high, low, close, volume)

    Raises:
        ValueError: If API key is missing or symbol is invalid
    """
    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        raise ValueError(
            "FINNHUB_API_KEY environment variable not set. "
            "Please set your Finnhub API key from https://finnhub.io"
        )

    if not symbol or len(symbol.strip()) == 0:
        raise ValueError("Symbol cannot be empty")

    symbol = symbol.strip().upper()
    if len(symbol) > 20:
        raise ValueError("Symbol cannot be longer than 20 characters")

    valid_resolutions = ["1", "5", "15", "30", "60", "D", "W", "M"]
    if resolution not in valid_resolutions:
        raise ValueError(f"Invalid resolution. Must be one of: {', '.join(valid_resolutions)}")

    if count < 1 or count > 500:
        raise ValueError("Count must be between 1 and 500")

    # Calculate date range
    end_time = int(datetime.now(timezone.utc).timestamp())
    
    # Map resolution to approximate days for count
    resolution_days = {
        "1": 1 / 24 / 60,      # 1 minute
        "5": 5 / 24 / 60,      # 5 minutes
        "15": 15 / 24 / 60,    # 15 minutes
        "30": 30 / 24 / 60,    # 30 minutes
        "60": 1 / 24,          # 1 hour
        "D": 1,                # 1 day
        "W": 7,                # 1 week
        "M": 30,               # 1 month
    }
    days_back = int(count * resolution_days.get(resolution, 1))
    start_time = int((datetime.now(timezone.utc) - timedelta(days=days_back)).timestamp())

    endpoint = "https://finnhub.io/api/v1/stock/candle"
    params = {
        "symbol": symbol,
        "resolution": resolution,
        "from": start_time,
        "to": end_time,
        "token": api_key,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            # Check if API returned an error
            if "error" in data:
                raise ValueError(f"Finnhub API error: {data['error']}")

            # Check if valid data returned
            if data.get("s") != "ok":
                raise ValueError(f"No candle data available for {symbol}")

            # Format candles
            candles = []
            timestamps = data.get("t", [])
            opens = data.get("o", [])
            highs = data.get("h", [])
            lows = data.get("l", [])
            closes = data.get("c", [])
            volumes = data.get("v", [])

            for i in range(len(timestamps)):
                candle = {
                    "timestamp": timestamps[i],
                    "open": opens[i],
                    "high": highs[i],
                    "low": lows[i],
                    "close": closes[i],
                    "volume": volumes[i],
                }
                candles.append(candle)

            formatted = {
                "symbol": symbol,
                "resolution": resolution,
                "candles": candles,
            }

            return formatted

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Finnhub API authentication failed. Check your API key.")
        elif e.response.status_code == 429:
            raise ValueError("Finnhub API rate limit exceeded. Try again later.")
        else:
            raise ValueError(f"Finnhub API request failed: {str(e)}")

    except httpx.RequestError as e:
        raise ValueError(f"Failed to connect to Finnhub API: {str(e)}")

    except Exception as e:
        raise ValueError(f"Error fetching stock candles: {str(e)}")


async def get_market_news(category: str = "general", min_id: int = 0) -> list[dict]:
    """
    Fetch market news using Finnhub /news endpoint.

    Args:
        category: News category (general, forex, crypto, merger)
        min_id: Minimum news ID for pagination (default 0)

    Returns:
        List of news articles with fields: id, category, headline, 
        summary, source, url, datetime, related_symbols

    Raises:
        ValueError: If API key is missing or category is invalid
    """
    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        raise ValueError(
            "FINNHUB_API_KEY environment variable not set. "
            "Please set your Finnhub API key from https://finnhub.io"
        )

    valid_categories = ["general", "forex", "crypto", "merger"]
    if category not in valid_categories:
        raise ValueError(f"Invalid category. Must be one of: {', '.join(valid_categories)}")

    endpoint = "https://finnhub.io/api/v1/news"
    params = {
        "category": category,
        "minId": min_id,
        "token": api_key,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            # Check if API returned an error
            if not isinstance(data, list):
                raise ValueError("Finnhub API returned unexpected response format")

            if not data:
                return []

            # Format articles
            formatted_articles = []
            for article in data:
                formatted_article = {
                    "id": article.get("id", 0),
                    "category": article.get("category", ""),
                    "headline": article.get("headline", ""),
                    "summary": article.get("summary", ""),
                    "source": article.get("source", ""),
                    "url": article.get("url", ""),
                    "datetime": article.get("datetime", 0),
                    "related_symbols": article.get("related", []),
                }
                formatted_articles.append(formatted_article)

            return formatted_articles

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Finnhub API authentication failed. Check your API key.")
        elif e.response.status_code == 429:
            raise ValueError("Finnhub API rate limit exceeded. Try again later.")
        else:
            raise ValueError(f"Finnhub API request failed: {str(e)}")

    except httpx.RequestError as e:
        raise ValueError(f"Failed to connect to Finnhub API: {str(e)}")

    except Exception as e:
        raise ValueError(f"Error fetching market news: {str(e)}")


async def get_index_quote(symbol: str) -> dict:
    """
    Fetch latest index quote (e.g., NIFTY, SENSEX) using Finnhub /quote endpoint.

    Args:
        symbol: Index symbol (e.g., "NSEI" for NIFTY, "BSESN" for SENSEX)

    Returns:
        Dict with fields: symbol, current_price, change, change_percent, 
                        high, low, open, previous_close, timestamp

    Raises:
        ValueError: If API key is missing or symbol is invalid
    """
    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        raise ValueError(
            "FINNHUB_API_KEY environment variable not set. "
            "Please set your Finnhub API key from https://finnhub.io"
        )

    if not symbol or len(symbol.strip()) == 0:
        raise ValueError("Symbol cannot be empty")

    symbol = symbol.strip().upper()
    if len(symbol) > 20:
        raise ValueError("Symbol cannot be longer than 20 characters")

    endpoint = "https://finnhub.io/api/v1/quote"
    params = {
        "symbol": symbol,
        "token": api_key,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            # Check if API returned an error
            if "error" in data:
                raise ValueError(f"Finnhub API error: {data['error']}")

            # Check if valid data returned
            if data.get("c") is None:
                raise ValueError(f"Invalid symbol or no data available for {symbol}")

            # Format response
            formatted = {
                "symbol": symbol,
                "current_price": data.get("c", 0),
                "change": data.get("d", 0),
                "change_percent": data.get("dp", 0),
                "high": data.get("h", 0),
                "low": data.get("l", 0),
                "open": data.get("o", 0),
                "previous_close": data.get("pc", 0),
                "timestamp": data.get("t", 0),
            }

            return formatted

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Finnhub API authentication failed. Check your API key.")
        elif e.response.status_code == 429:
            raise ValueError("Finnhub API rate limit exceeded. Try again later.")
        else:
            raise ValueError(f"Finnhub API request failed: {str(e)}")

    except httpx.RequestError as e:
        raise ValueError(f"Failed to connect to Finnhub API: {str(e)}")

    except Exception as e:
        raise ValueError(f"Error fetching index quote: {str(e)}")


async def build_market_context() -> dict[str, Any]:
    """
    Build a market context object containing index data, market direction, and news headlines.

    Returns:
        Dict with fields:
        - market_direction: "up", "down", or "flat" based on NIFTY change
        - nifty: NIFTY index data (current_price, change, change_percent)
        - sensex: SENSEX index data (current_price, change, change_percent)
        - news_headlines: List of recent market news headlines
        - timestamp: Current timestamp
    """
    from news_fetcher import fetch_financial_news

    context = {
        "market_direction": "flat",
        "nifty": None,
        "sensex": None,
        "news_headlines": [],
        "timestamp": int(datetime.now(timezone.utc).timestamp()),
    }

    # Fetch NIFTY data
    try:
        nifty = await get_index_quote("NSEI")
        context["nifty"] = {
            "current_price": nifty.get("current_price"),
            "change": nifty.get("change"),
            "change_percent": nifty.get("change_percent"),
        }
        if nifty.get("change_percent", 0) > 0.1:
            context["market_direction"] = "up"
        elif nifty.get("change_percent", 0) < -0.1:
            context["market_direction"] = "down"
    except Exception as e:
        print(f"[Market Context] Failed to fetch NIFTY: {e}")

    # Fetch SENSEX data
    try:
        sensex = await get_index_quote("BSESN")
        context["sensex"] = {
            "current_price": sensex.get("current_price"),
            "change": sensex.get("change"),
            "change_percent": sensex.get("change_percent"),
        }
    except Exception as e:
        print(f"[Market Context] Failed to fetch SENSEX: {e}")

    # Fetch market news
    try:
        news = await fetch_financial_news("Indian stock market NIFTY SENSEX", max_articles=5)
        context["news_headlines"] = [
            {"title": article.get("title", ""), "source": article.get("source", "")}
            for article in news[:5]
        ]
    except Exception as e:
        print(f"[Market Context] Failed to fetch news: {e}")

    return context


async def _fetch_top_movers(symbols: list[str], top_n: int = 5) -> dict[str, list[dict]]:
    """
    Fetch quotes for a list of symbols and return top gainers and losers.
    """
    import asyncio

    results: list[dict] = []

    async def _safe_quote(sym: str) -> dict | None:
        try:
            return await get_stock_quote(sym)
        except Exception:
            return None

    quotes = await asyncio.gather(*[_safe_quote(s) for s in symbols])

    for q in quotes:
        if q and q.get("current_price") and q.get("change_percent") is not None:
            results.append(q)

    # Sort by change_percent
    results.sort(key=lambda x: x.get("change_percent", 0), reverse=True)

    gainers = [
        {
            "symbol": r["symbol"],
            "price": r["current_price"],
            "change_percent": round(r["change_percent"], 2),
        }
        for r in results[:top_n]
        if r.get("change_percent", 0) > 0
    ]

    losers = [
        {
            "symbol": r["symbol"],
            "price": r["current_price"],
            "change_percent": round(r["change_percent"], 2),
        }
        for r in results[-top_n:]
        if r.get("change_percent", 0) < 0
    ]
    losers.reverse()  # worst first

    return {"gainers": gainers, "losers": losers}


async def build_enriched_market_context(
    symbols: list[str] | None = None,
    stock_names: list[str] | None = None,
) -> dict[str, Any]:
    """
    Build a rich market context with index data, top movers, stock-specific
    quotes, and news — designed to feed the copilot LLM with actionable data.

    Args:
        symbols: Optional list of Finnhub symbols the user asked about.
        stock_names: Optional list of human-readable stock names (for news queries).

    Returns:
        Dict with all fields from build_market_context() plus:
        - top_gainers: Top gaining NIFTY stocks
        - top_losers: Top losing NIFTY stocks
        - stock_quotes: Quotes for specifically mentioned stocks
        - data_summary: Human-readable text digest for the LLM
    """
    from market_query_analyzer import TOP_NIFTY_SYMBOLS
    from news_fetcher import fetch_financial_news
    import asyncio

    # Start with basic market context
    base_ctx = await build_market_context()

    enriched = {**base_ctx}
    enriched["top_gainers"] = []
    enriched["top_losers"] = []
    enriched["stock_quotes"] = {}

    # Fetch top movers from curated NIFTY 50 list
    try:
        movers = await _fetch_top_movers(TOP_NIFTY_SYMBOLS, top_n=5)
        enriched["top_gainers"] = movers.get("gainers", [])
        enriched["top_losers"] = movers.get("losers", [])
    except Exception as e:
        print(f"[Enriched Context] Failed to fetch top movers: {e}")

    # Fetch specific stock quotes if symbols were mentioned
    if symbols:
        # Exclude symbols already in the top movers list
        extra_symbols = [s for s in symbols if s not in TOP_NIFTY_SYMBOLS]
        all_symbols = symbols  # fetch all mentioned, even if in NIFTY list

        async def _safe_quote(sym: str) -> tuple[str, dict | None]:
            try:
                q = await get_stock_quote(sym)
                return sym, q
            except Exception:
                return sym, None

        results = await asyncio.gather(*[_safe_quote(s) for s in all_symbols])
        for sym, q in results:
            if q:
                enriched["stock_quotes"][sym] = {
                    "symbol": sym,
                    "price": q.get("current_price"),
                    "change": q.get("change"),
                    "change_percent": round(q.get("change_percent", 0), 2),
                    "high": q.get("high"),
                    "low": q.get("low"),
                    "open": q.get("open"),
                    "previous_close": q.get("previous_close"),
                }

        # Fetch stock-specific news
        if stock_names:
            try:
                query = " OR ".join(stock_names[:3]) + " stock India"
                stock_news = await fetch_financial_news(query, max_articles=5)
                enriched["stock_news"] = [
                    {"title": a.get("title", ""), "source": a.get("source", "")}
                    for a in stock_news[:5]
                ]
            except Exception as e:
                print(f"[Enriched Context] Failed to fetch stock news: {e}")

    # Build human-readable summary for the LLM
    enriched["data_summary"] = _build_data_summary(enriched)

    return enriched


def _build_data_summary(ctx: dict) -> str:
    """Build a concise human-readable summary of the market data."""
    parts: list[str] = []

    direction = ctx.get("market_direction", "flat").upper()
    parts.append(f"MARKET DIRECTION: {direction}")

    # Index data
    nifty = ctx.get("nifty")
    if nifty and nifty.get("current_price"):
        parts.append(
            f"NIFTY 50: ₹{nifty['current_price']:,.2f} "
            f"({nifty.get('change_percent', 0):+.2f}%)"
        )

    sensex = ctx.get("sensex")
    if sensex and sensex.get("current_price"):
        parts.append(
            f"SENSEX: ₹{sensex['current_price']:,.2f} "
            f"({sensex.get('change_percent', 0):+.2f}%)"
        )

    # Top movers
    gainers = ctx.get("top_gainers", [])
    if gainers:
        g_str = ", ".join(
            f"{g['symbol'].replace('.NS','')} ({g['change_percent']:+.2f}%)"
            for g in gainers[:5]
        )
        parts.append(f"TOP GAINERS: {g_str}")

    losers = ctx.get("top_losers", [])
    if losers:
        l_str = ", ".join(
            f"{l['symbol'].replace('.NS','')} ({l['change_percent']:+.2f}%)"
            for l in losers[:5]
        )
        parts.append(f"TOP LOSERS: {l_str}")

    # Stock-specific data
    stock_quotes = ctx.get("stock_quotes", {})
    if stock_quotes:
        for sym, q in stock_quotes.items():
            parts.append(
                f"{sym.replace('.NS','')}: ₹{q['price']:,.2f} "
                f"({q['change_percent']:+.2f}%), "
                f"Open: ₹{q.get('open', 0):,.2f}, "
                f"High: ₹{q.get('high', 0):,.2f}, "
                f"Low: ₹{q.get('low', 0):,.2f}"
            )

    # Headlines
    headlines = ctx.get("news_headlines", [])
    stock_news = ctx.get("stock_news", [])
    all_headlines = headlines + stock_news
    if all_headlines:
        parts.append("RECENT HEADLINES:")
        for i, h in enumerate(all_headlines[:8], 1):
            parts.append(f"  {i}. {h.get('title', 'N/A')} — {h.get('source', 'Unknown')}")

    return "\n".join(parts)
