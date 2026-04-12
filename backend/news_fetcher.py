"""
News Fetcher Module

Fetches financial news articles from NewsAPI based on user queries.
"""

import os
import httpx
from typing import Optional
from datetime import datetime, timedelta


def _indian_context_boost(q: str) -> str:
    """Widen NewsAPI queries toward Indian markets when relevant."""
    lower = q.lower()
    triggers = (
        "nifty", "sensex", "nse", "bse", "india", "indian", "inr", "rupee",
        "rbi", "sebi", "reliance", "tcs", "hdfc", "infosys", "itc", "l&t",
        "bank nifty", "banknifty", "fii", "dii",
    )
    if any(t in lower for t in triggers):
        return f"({q}) AND (India OR NSE OR BSE OR Sensex OR Nifty)"
    return q


async def fetch_financial_news(query: str, max_articles: int = 10) -> list[dict]:
    """
    Fetch financial news articles from NewsAPI.

    Args:
        query: Search query (e.g., "Apple stock" or "market falling")
        max_articles: Maximum number of articles to return (default 10)

    Returns:
        List of articles with fields: title, description, source, url, publishedAt

    Raises:
        ValueError: If API key is missing or query is invalid
    """

    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        raise ValueError(
            "NEWSAPI_KEY environment variable not set. "
            "Please set your NewsAPI key from https://newsapi.org"
        )

    # Validate query
    if not query or len(query.strip()) == 0:
        raise ValueError("Query cannot be empty")

    if len(query) > 200:
        raise ValueError("Query cannot be longer than 200 characters")

    boosted = _indian_context_boost(query.strip())

    # Prepare API request
    endpoint = "https://newsapi.org/v2/everything"
    params = {
        "q": boosted,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": max_articles,
        "apiKey": api_key,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(endpoint, params=params)
            response.raise_for_status()

            data = response.json()

            # Check if API returned an error
            if data.get("status") == "error":
                error_code = data.get("code")
                error_msg = data.get("message", "Unknown error")

                if error_code == "apiKeyInvalid":
                    raise ValueError("NewsAPI key is invalid")
                elif error_code == "rateLimited":
                    raise ValueError("NewsAPI rate limit exceeded. Try again later.")
                else:
                    raise ValueError(f"NewsAPI error: {error_msg}")

            # Extract articles
            articles = data.get("articles", [])

            if not articles:
                return []

            # Format articles
            formatted_articles = []
            for article in articles:
                formatted_article = {
                    "title": article.get("title", ""),
                    "description": article.get("description", "") or article.get("content", ""),
                    "source": article.get("source", {}).get("name", "Unknown"),
                    "url": article.get("url", ""),
                    "published_at": article.get("publishedAt", ""),
                    "content": article.get("content", ""),
                }
                formatted_articles.append(formatted_article)

            return formatted_articles

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("NewsAPI authentication failed. Check your API key.")
        elif e.response.status_code == 429:
            raise ValueError("NewsAPI rate limit exceeded. Try again later.")
        else:
            raise ValueError(f"NewsAPI request failed: {str(e)}")

    except httpx.RequestError as e:
        raise ValueError(f"Failed to connect to NewsAPI: {str(e)}")

    except Exception as e:
        raise ValueError(f"Error fetching news: {str(e)}")
