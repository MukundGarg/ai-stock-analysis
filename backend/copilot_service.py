"""
Unified trading copilot: one conversation brain with optional workspace context from tools.
"""

from __future__ import annotations

import json
import os
import uuid
from collections import defaultdict
from typing import Any

from indian_market_context import INDIAN_MARKETS_REFERENCE
from ai_provider import get_llm
from ai_provider.config import get_provider_name
from ai_provider.constants import GEMINI_MODEL

_MAX_TURNS = 24
_MAX_MESSAGE_CHARS = 4000

_sessions: dict[str, list[dict[str, str]]] = defaultdict(list)


def _trim_session(messages: list[dict[str, str]]) -> list[dict[str, str]]:
    if len(messages) <= _MAX_TURNS:
        return messages
    return messages[-_MAX_TURNS:]


def _system_prompt(workspace_context: dict[str, Any] | None) -> str:
    base = f"""You are **BharatTrade Copilot**, an intelligent Indian-market-focused trading assistant inside a stock learning app.

## Your Core Rules

1. **For market questions** (e.g. "Why is the market up?", "What is driving NIFTY?", "Why is Reliance falling?"):
   - You MUST base your response on the **LIVE MARKET DATA** provided below.
   - Reference **specific numbers**: index levels, percentage changes, stock prices, top gainers/losers.
   - Cite **actual news headlines** from the data when explaining market movements.
   - Explain movements like a **market analyst giving a daily briefing** — confident, data-backed, insightful.
   - Connect the dots between data points: e.g. "NIFTY is up 1.2% driven by banking stocks — HDFC Bank gained 2.3% and ICICI rose 1.8%, likely on expectations of strong Q4 results."

2. **NEVER say any of the following**:
   - "I'm not aware of the current market situation"
   - "I don't have access to real-time data"
   - "There could be many reasons..."
   - "I cannot provide real-time information"
   You have live data — USE IT. If some data is missing, work with what is available and note the limitation briefly.

3. **For educational/general questions** (e.g. "What is F&O?", "Explain P/E ratio"):
   - Use **simple, beginner-friendly** language; define jargon briefly.
   - Stay accurate; if uncertain, say so.

4. **For "Should I buy?" type questions**:
   - **Do not give personalized buy/sell instructions**.
   - Explain **how to think about the decision**, risks, and that they should consult SEBI-registered advisors.

5. **Never invent data**. Only use the market data provided below. Never fabricate prices, percentages, or news.

{INDIAN_MARKETS_REFERENCE}
"""

    if workspace_context:
        try:
            # Check if enriched market data is available
            if "market_data" in workspace_context:
                market_data = workspace_context["market_data"]

                # Use the pre-built data summary if available (much clearer for the LLM)
                data_summary = market_data.get("data_summary", "")
                if data_summary:
                    base += f"""
## ═══ LIVE MARKET DATA (use this to answer market questions) ═══

{data_summary}

═══ END LIVE DATA ═══

**IMPORTANT**: When answering market questions, you MUST reference the specific data above. Quote actual numbers, name actual stocks, and cite actual headlines.
"""
                else:
                    # Fallback to structured display if no summary
                    market_section = f"""
## ═══ LIVE MARKET DATA ═══
- Market Direction: {market_data.get('market_direction', 'unknown').upper()}
"""
                    nifty = market_data.get('nifty', {})
                    if nifty and nifty.get('current_price'):
                        market_section += f"- NIFTY: ₹{nifty.get('current_price', 'N/A')} (Change: {nifty.get('change_percent', 0):.2f}%)\n"

                    sensex = market_data.get('sensex', {})
                    if sensex and sensex.get('current_price'):
                        market_section += f"- SENSEX: ₹{sensex.get('current_price', 'N/A')} (Change: {sensex.get('change_percent', 0):.2f}%)\n"

                    # Top movers
                    top_gainers = market_data.get('top_gainers', [])
                    if top_gainers:
                        market_section += "\n### Top Gainers Today\n"
                        for g in top_gainers[:5]:
                            market_section += f"- {g.get('symbol', '').replace('.NS', '')}: ₹{g.get('price', 0):,.2f} ({g.get('change_percent', 0):+.2f}%)\n"

                    top_losers = market_data.get('top_losers', [])
                    if top_losers:
                        market_section += "\n### Top Losers Today\n"
                        for l in top_losers[:5]:
                            market_section += f"- {l.get('symbol', '').replace('.NS', '')}: ₹{l.get('price', 0):,.2f} ({l.get('change_percent', 0):+.2f}%)\n"

                    # Stock-specific quotes
                    stock_quotes = market_data.get('stock_quotes', {})
                    if stock_quotes:
                        market_section += "\n### Stocks User Asked About\n"
                        for sym, q in stock_quotes.items():
                            market_section += (
                                f"- {sym.replace('.NS', '')}: ₹{q.get('price', 0):,.2f} "
                                f"({q.get('change_percent', 0):+.2f}%), "
                                f"Open: ₹{q.get('open', 0):,.2f}, "
                                f"High: ₹{q.get('high', 0):,.2f}, "
                                f"Low: ₹{q.get('low', 0):,.2f}\n"
                            )

                    # Headlines
                    headlines = market_data.get('news_headlines', [])
                    stock_news = market_data.get('stock_news', [])
                    all_headlines = headlines + stock_news
                    if all_headlines:
                        market_section += "\n### Recent Market Headlines\n"
                        for i, headline in enumerate(all_headlines[:8], 1):
                            market_section += f"{i}. {headline.get('title', '')} ({headline.get('source', 'Unknown')})\n"

                    market_section += "\n═══ END LIVE DATA ═══\n"
                    base += market_section

                # Add other workspace context (PDF analysis, chart analysis etc.)
                other_context = {k: v for k, v in workspace_context.items() if k != 'market_data'}
                if other_context:
                    ctx = json.dumps(other_context, ensure_ascii=False, indent=2)[:12000]
                    base += f"""
### Current workspace context (from the user's recent tool runs — use only as background; user may ask follow-ups)
```json
{ctx}
```
"""
            else:
                ctx = json.dumps(workspace_context, ensure_ascii=False, indent=2)[:12000]
                base += f"""

### Current workspace context (from the user's recent tool runs — use only as background; user may ask follow-ups)
```json
{ctx}
```
"""
        except Exception:
            ctx = str(workspace_context)[:12000]
            base += f"""

### Current workspace context (from the user's recent tool runs — use only as background; user may ask follow-ups)
```json
{ctx}
```
"""
    return base


def new_session_id() -> str:
    return str(uuid.uuid4())


def _default_copilot_model() -> str:
    if os.getenv("COPILOT_MODEL"):
        return os.getenv("COPILOT_MODEL", "").strip()
    if get_provider_name() == "groq":
        return os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
    return os.getenv("GEMINI_MODEL", GEMINI_MODEL).strip()


def copilot_chat(
    message: str,
    session_id: str | None,
    workspace_context: dict[str, Any] | None,
) -> tuple[str, str, str]:
    """
    Returns (reply, session_id, model_used).
    """
    text = (message or "").strip()
    if not text:
        raise ValueError("Message cannot be empty")
    if len(text) > _MAX_MESSAGE_CHARS:
        raise ValueError(f"Message too long (max {_MAX_MESSAGE_CHARS} characters)")

    sid = session_id or new_session_id()
    llm = get_llm()

    history = _sessions[sid]
    history.append({"role": "user", "content": text})
    history = _trim_session(history)

    model = _default_copilot_model()
    messages = [{"role": "system", "content": _system_prompt(workspace_context)}] + history

    reply = llm.chat(
        messages,
        model=model,
        temperature=0.5,
        max_tokens=1200,
    )
    reply = (reply or "").strip()
    if not reply:
        reply = "I couldn’t generate a reply. Please try rephrasing your question."

    history.append({"role": "assistant", "content": reply})
    _sessions[sid] = _trim_session(history)

    return reply, sid, model
