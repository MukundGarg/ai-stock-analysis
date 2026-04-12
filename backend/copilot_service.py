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

_MAX_TURNS = 24
_MAX_MESSAGE_CHARS = 4000

_sessions: dict[str, list[dict[str, str]]] = defaultdict(list)


def _trim_session(messages: list[dict[str, str]]) -> list[dict[str, str]]:
    if len(messages) <= _MAX_TURNS:
        return messages
    return messages[-_MAX_TURNS:]


def _system_prompt(workspace_context: dict[str, Any] | None) -> str:
    base = f"""You are **BharatTrade Copilot**, a single intelligent assistant inside an Indian-market-focused stock learning app.

Your role:
- Answer questions about **Indian markets (NSE, BSE)**, stocks, F&O basics, risk, and how to read outputs from this app (PDF reports, chart patterns, sentiment).
- Use **simple, beginner-friendly** language; define jargon briefly when you use it.
- When users ask "Should I buy?": **do not give personalized buy/sell instructions**. Explain **how to think about the decision**, risks, position sizing concepts, and that they should use SEBI-registered advisors for advice.
- Stay accurate; if uncertain, say so. Never invent live prices or guaranteed returns.

{INDIAN_MARKETS_REFERENCE}
"""
    if workspace_context:
        try:
            ctx = json.dumps(workspace_context, ensure_ascii=False, indent=2)[:12000]
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
    return os.getenv("GEMINI_MODEL", "gemini-2.0-flash").strip()


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
