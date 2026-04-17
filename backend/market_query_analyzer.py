"""
Market Query Analyzer

Classifies user messages to detect market-related questions, extracts mentioned
stock symbols, and determines the question type so the copilot can fetch the
right live data before answering.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Common Indian stock name → Finnhub symbol mapping
# ---------------------------------------------------------------------------
STOCK_NAME_TO_SYMBOL: dict[str, str] = {
    # Large-cap / NIFTY 50 stalwarts
    "reliance": "RELIANCE.NS",
    "ril": "RELIANCE.NS",
    "tcs": "TCS.NS",
    "infosys": "INFY.NS",
    "infy": "INFY.NS",
    "hdfc bank": "HDFCBANK.NS",
    "hdfcbank": "HDFCBANK.NS",
    "hdfc": "HDFCBANK.NS",
    "icici bank": "ICICIBANK.NS",
    "icici": "ICICIBANK.NS",
    "sbi": "SBIN.NS",
    "state bank": "SBIN.NS",
    "kotak": "KOTAKBANK.NS",
    "kotak bank": "KOTAKBANK.NS",
    "axis bank": "AXISBANK.NS",
    "axis": "AXISBANK.NS",
    "itc": "ITC.NS",
    "wipro": "WIPRO.NS",
    "hcl tech": "HCLTECH.NS",
    "hcltech": "HCLTECH.NS",
    "hcl": "HCLTECH.NS",
    "bharti airtel": "BHARTIARTL.NS",
    "airtel": "BHARTIARTL.NS",
    "bajaj finance": "BAJFINANCE.NS",
    "bajaj finserv": "BAJAJFINSV.NS",
    "bajaj auto": "BAJAJ-AUTO.NS",
    "maruti": "MARUTI.NS",
    "maruti suzuki": "MARUTI.NS",
    "tata motors": "TATAMOTORS.NS",
    "tata steel": "TATASTEEL.NS",
    "tata power": "TATAPOWER.NS",
    "tata": "TATAMOTORS.NS",  # default Tata to Tata Motors
    "sun pharma": "SUNPHARMA.NS",
    "asian paints": "ASIANPAINT.NS",
    "ultratech": "ULTRACEMCO.NS",
    "ultratech cement": "ULTRACEMCO.NS",
    "nestle": "NESTLEIND.NS",
    "hindustan unilever": "HINDUNILVR.NS",
    "hul": "HINDUNILVR.NS",
    "larsen": "LT.NS",
    "l&t": "LT.NS",
    "lt": "LT.NS",
    "tech mahindra": "TECHM.NS",
    "m&m": "M&M.NS",
    "mahindra": "M&M.NS",
    "power grid": "POWERGRID.NS",
    "ntpc": "NTPC.NS",
    "ongc": "ONGC.NS",
    "adani enterprises": "ADANIENT.NS",
    "adani ports": "ADANIPORTS.NS",
    "adani": "ADANIENT.NS",
    "cipla": "CIPLA.NS",
    "dr reddy": "DRREDDY.NS",
    "dr reddys": "DRREDDY.NS",
    "divis lab": "DIVISLAB.NS",
    "titan": "TITAN.NS",
    "coal india": "COALINDIA.NS",
    "grasim": "GRASIM.NS",
    "hero motocorp": "HEROMOTOCO.NS",
    "hero": "HEROMOTOCO.NS",
    "eicher motors": "EICHERMOT.NS",
    "eicher": "EICHERMOT.NS",
    "britannia": "BRITANNIA.NS",
    "indusind bank": "INDUSINDBK.NS",
    "indusind": "INDUSINDBK.NS",
    "vedanta": "VEDL.NS",
    "jsw steel": "JSWSTEEL.NS",
    "jsw": "JSWSTEEL.NS",
    "hindalco": "HINDALCO.NS",
    "zomato": "ZOMATO.NS",
}

# Index synonyms
INDEX_SYNONYMS: dict[str, str] = {
    "nifty": "NIFTY",
    "nifty 50": "NIFTY",
    "nifty50": "NIFTY",
    "sensex": "SENSEX",
    "bank nifty": "BANKNIFTY",
    "banknifty": "BANKNIFTY",
    "nifty bank": "BANKNIFTY",
}

# A curated set of major NIFTY 50 stocks used to compute top movers
TOP_NIFTY_SYMBOLS: list[str] = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "KOTAKBANK.NS", "LT.NS",
    "AXISBANK.NS", "BAJFINANCE.NS", "MARUTI.NS", "TATAMOTORS.NS",
    "SUNPHARMA.NS", "TITAN.NS", "HCLTECH.NS", "WIPRO.NS", "NTPC.NS",
    "POWERGRID.NS", "TATASTEEL.NS", "ADANIENT.NS", "HINDUNILVR.NS",
    "ASIANPAINT.NS", "M&M.NS",
]

# ---------------------------------------------------------------------------
# Keywords / patterns for question classification
# ---------------------------------------------------------------------------
_MARKET_KEYWORDS: list[str] = [
    "market", "nifty", "sensex", "index", "up today", "down today",
    "falling", "rising", "why is", "what is driving", "stock market",
    "trend", "movement", "gainers", "losers", "rally", "crash", "correction",
    "bull", "bear", "green", "red", "blood bath", "bloodbath",
    "fii", "dii", "foreign", "institutional",
    "market today", "today market", "what happened",
    "bank nifty", "banknifty", "midcap", "smallcap",
    "sector", "pharma", "it sector", "auto sector", "metal", "banking",
]

_STOCK_ACTION_PATTERNS: list[re.Pattern] = [
    re.compile(r"why\s+is\s+(\w[\w\s&]*?)\s+(up|down|falling|rising|moving|crashing|rallying|dropping|surging)", re.I),
    re.compile(r"what(?:'s| is)\s+happening\s+(?:with|to)\s+(\w[\w\s&]*)", re.I),
    re.compile(r"(\w[\w\s&]*?)\s+(?:stock|share)\s+(?:price|movement|trend)", re.I),
    re.compile(r"tell\s+me\s+about\s+(\w[\w\s&]*?)\s+(?:stock|share|today)", re.I),
]


@dataclass
class QueryAnalysis:
    """Result of analyzing a user message."""
    is_market_question: bool = False
    question_type: str = "general"  # market_overview | stock_specific | index_specific | general
    mentioned_symbols: list[str] = field(default_factory=list)
    mentioned_indices: list[str] = field(default_factory=list)
    raw_stock_names: list[str] = field(default_factory=list)


def analyze_query(message: str) -> QueryAnalysis:
    """
    Analyze a user message and return classification + extracted symbols.
    """
    if not message or not message.strip():
        return QueryAnalysis()

    text = message.strip()
    lower = text.lower()
    result = QueryAnalysis()

    # 1. Check for market keywords
    for kw in _MARKET_KEYWORDS:
        if kw in lower:
            result.is_market_question = True
            break

    # 2. Check for index mentions
    for synonym, index_name in INDEX_SYNONYMS.items():
        if synonym in lower:
            result.is_market_question = True
            if index_name not in result.mentioned_indices:
                result.mentioned_indices.append(index_name)

    # 3. Extract stock names via pattern matching
    for pattern in _STOCK_ACTION_PATTERNS:
        match = pattern.search(text)
        if match:
            name = match.group(1).strip().lower()
            result.is_market_question = True
            if name in STOCK_NAME_TO_SYMBOL:
                symbol = STOCK_NAME_TO_SYMBOL[name]
                if symbol not in result.mentioned_symbols:
                    result.mentioned_symbols.append(symbol)
                    result.raw_stock_names.append(name.title())

    # 4. Direct stock name lookup in message
    for name, symbol in STOCK_NAME_TO_SYMBOL.items():
        # Use word boundary check to avoid partial matches
        # For multi-word names, check directly; for single words, use boundary
        if len(name) <= 2:
            continue  # skip very short abbreviations that cause false positives
        if f" {name} " in f" {lower} " or lower.startswith(f"{name} ") or lower.endswith(f" {name}"):
            result.is_market_question = True
            if symbol not in result.mentioned_symbols:
                result.mentioned_symbols.append(symbol)
                result.raw_stock_names.append(name.title())

    # 5. Determine question type
    if result.mentioned_symbols:
        result.question_type = "stock_specific"
    elif result.mentioned_indices:
        result.question_type = "index_specific"
    elif result.is_market_question:
        result.question_type = "market_overview"
    else:
        result.question_type = "general"

    return result
