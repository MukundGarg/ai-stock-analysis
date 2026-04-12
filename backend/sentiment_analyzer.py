"""
Sentiment Analyzer Module

Uses VADER sentiment analysis to analyze news articles and determine market sentiment.
"""

from typing import Dict, Any, List
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import re

# Download required VADER lexicon
try:
    nltk.data.find("vader_lexicon")
except LookupError:
    nltk.download("vader_lexicon", quiet=True)

# Initialize VADER analyzer (singleton)
sia = SentimentIntensityAnalyzer()


def analyze_sentiment(articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze sentiment of news articles using VADER.

    Args:
        articles: List of articles with title, description, content fields

    Returns:
        Dictionary with:
        - overall_sentiment: "Bullish", "Bearish", or "Neutral"
        - sentiment_score: -1.0 to 1.0 (compound VADER score)
        - key_reasons: List of main themes extracted from articles
        - article_sentiments: List of sentiments for each article
    """

    if not articles:
        return {
            "overall_sentiment": "Neutral",
            "sentiment_score": 0.0,
            "key_reasons": [],
            "article_sentiments": [],
        }

    # Score each article
    article_sentiments = []
    scores = []

    for article in articles:
        # Combine title and description for analysis
        text_to_analyze = f"{article.get('title', '')} {article.get('description', '')}"

        if not text_to_analyze.strip():
            continue

        # Get VADER sentiment
        scores_dict = sia.polarity_scores(text_to_analyze)
        compound_score = scores_dict["compound"]  # -1 to 1
        scores.append(compound_score)

        # Determine sentiment label
        if compound_score > 0.2:
            sentiment = "Bullish"
        elif compound_score < -0.2:
            sentiment = "Bearish"
        else:
            sentiment = "Neutral"

        article_sentiments.append({
            "title": article.get("title", ""),
            "sentiment_score": round(compound_score, 3),
            "sentiment": sentiment,
        })

    # Calculate overall sentiment
    if scores:
        average_score = sum(scores) / len(scores)
    else:
        average_score = 0.0

    if average_score > 0.1:
        overall_sentiment = "Bullish"
    elif average_score < -0.1:
        overall_sentiment = "Bearish"
    else:
        overall_sentiment = "Neutral"

    # Extract key themes/reasons
    key_reasons = extract_themes(articles)

    return {
        "overall_sentiment": overall_sentiment,
        "sentiment_score": round(average_score, 3),
        "key_reasons": key_reasons,
        "article_sentiments": article_sentiments,
    }


def extract_themes(articles: List[Dict[str, Any]]) -> List[str]:
    """
    Extract key themes/reasons from article titles and descriptions.

    Args:
        articles: List of articles

    Returns:
        List of 2-3 key themes found in the news
    """

    # Define keywords that indicate themes
    theme_keywords = {
        # Positive themes
        "growth": ["growth", "surge", "rally", "bull", "strong", "rising", "upbeat", "gain", "profit"],
        "earnings": ["earnings", "profit", "revenue", "dividend", "beat", "performance", "results"],
        "innovation": ["innovation", "new product", "launch", "breakthrough", "technology", "ai", "advance"],

        # Negative themes
        "decline": ["decline", "fall", "collapse", "crash", "lost", "loss", "slump", "down", "bear"],
        "economic": ["recession", "inflation", "slowdown", "economic", "gdp", "unemployment", "crisis"],
        "concern": ["concern", "risk", "warning", "threat", "danger", "troubled", "struggle", "weak"],

        # Neutral/Market themes
        "regulation": ["regulation", "sec", "law", "compliance", "government", "policy"],
        "competition": ["competition", "rival", "market share", "compete"],
        "market": ["market", "sector", "index", "volatility", "trading"],
    }

    theme_counts = {theme: 0 for theme in theme_keywords}

    # Count keyword occurrences
    combined_text = ""
    for article in articles:
        combined_text += f" {article.get('title', '')} {article.get('description', '')} "

    combined_text_lower = combined_text.lower()

    for theme, keywords in theme_keywords.items():
        for keyword in keywords:
            # Count occurrences (case-insensitive)
            count = len(re.findall(r"\b" + re.escape(keyword) + r"\b", combined_text_lower))
            theme_counts[theme] += count

    # Get top 3 themes
    sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
    top_themes = [theme for theme, count in sorted_themes[:3] if count > 0]

    # Format theme names to be more readable
    readable_themes = []
    theme_descriptions = {
        "growth": "Positive market movement indicators",
        "earnings": "Company earnings and financial results",
        "innovation": "New products and technological advances",
        "decline": "Market decline and price drops",
        "economic": "Economic conditions and slowdown",
        "concern": "Market concerns and risks",
        "regulation": "Regulatory and government actions",
        "competition": "Competitive pressures",
        "market": "Market trends and volatility",
    }

    for theme in top_themes:
        readable_themes.append(theme_descriptions.get(theme, theme))

    # If less than 2 themes found, add generic description
    if len(readable_themes) < 2:
        readable_themes.append("Current market sentiment and dynamics")

    return readable_themes[:3]  # Return max 3 themes
