"""
Reference context for Indian equity markets — injected into the copilot system prompt
and exposed via /learn/indian-markets for the UI.
"""

INDIAN_MARKETS_REFERENCE = """
## Indian markets (quick reference for answers)

### Exchanges
- **NSE (National Stock Exchange)**: Largest Indian exchange by turnover; flagship index **NIFTY 50** (50 large caps).
- **BSE (Bombay Stock Exchange)**: Asia’s oldest; flagship **SENSEX** (30 large caps). Same underlying stocks often trade on both; prices stay aligned via arbitrage.

### Cash market hours (typical; verify on exchange notices)
- **Pre-open**: ~09:00–09:15 IST (order entry, price discovery).
- **Regular session**: **09:15–15:30 IST** (Monday–Friday, excluding holidays).
- **No US-style extended retail session** like US equities; after-hours is limited for most retail investors.

### F&O vs equity (cash)
- **Equity (cash)**: Buy/sell shares; pay full value (or margin in MIS/bo for intraday per broker). Long-term holding = capital gains rules (LTCG/STCG) — explain generally, not as tax advice.
- **Futures & Options (F&O)**: Derivatives on indices (e.g., NIFTY, BANKNIFTY) or stock options. **Higher risk**, leverage, expiry (weekly/monthly). Not suitable for most beginners; SEBI has eligibility norms (income/net worth thresholds) — keep explanation high-level.

### SEBI (simplified)
- **SEBI** regulates Indian securities markets: investor protection, disclosure norms for listed companies, broker regulations, action against manipulation. Listed companies publish results, related-party deals, etc. per SEBI/listing rules.

### Behaviour vs US markets
- India is **emerging market**: can be more volatile, sensitive to **FII/DII flows**, **RBI policy**, **crude**, **monsoon** (for some sectors), **global risk sentiment**.
- **US Fed/rates** and **USD/INR** often spill over; **Adrs/GDRs** are a minor link for some names.
- **Retail participation** has grown via UPI/discount brokers; **intraday** and **options** volume is large — remind beginners of risk.

### Beginner-friendly Indian examples (for illustrations only, not recommendations)
- Large, liquid names often cited in education: **Reliance**, **TCS**, **HDFC Bank** (illustrative examples only).

### Disclaimers (always reinforce)
- Not financial advice; user should verify with SEBI-registered advisors; past patterns don’t guarantee future results.
"""

INDIAN_MARKETS_STRUCTURED = {
    "title": "Indian market essentials",
    "exchanges": {
        "NSE": "National Stock Exchange; NIFTY 50 is the key 50-stock benchmark.",
        "BSE": "Bombay Stock Exchange; SENSEX tracks 30 large-cap stocks.",
    },
    "typical_trading_hours_ist": {
        "pre_open": "09:00–09:15 (order collection / indicative equilibrium)",
        "regular": "09:15–15:30, Monday–Friday (exchange holidays excepted)",
    },
    "fno_vs_equity": {
        "equity": "Ownership of shares in the cash market; long-term vs intraday depends on holding and broker product (e.g., CNC vs MIS).",
        "fno": "Contracts with expiry; leverage and asymmetric payoffs (especially options). Higher complexity and risk.",
    },
    "sebi_role": "Market regulator: disclosures, fair practices, investor protection frameworks.",
    "india_vs_us": [
        "Macro sensitivity: RBI, crude, INR, monsoon (select sectors), FII flows.",
        "Session structure differs from US; liquidity concentrated in regular hours.",
    ],
    "example_tickers_education_only": ["RELIANCE", "TCS", "HDFC BANK"],
}
