"""
AI Analyzer Module

Uses OpenAI API to analyze financial reports and provide beginner-friendly insights.
"""

import os
import json
import re
from typing import Dict, Any
from openai import OpenAI, APIError


# Initialize OpenAI client
def get_openai_client():
    """Get OpenAI client with API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable not set. "
            "Please set your OpenAI API key."
        )
    return OpenAI(api_key=api_key)


def analyze_financial_report(text: str) -> Dict[str, Any]:
    """
    Analyze financial report text using OpenAI GPT and return structured insights.

    Args:
        text: Cleaned extracted text from PDF

    Returns:
        Dictionary with analysis results containing:
        - company_summary: Brief company overview
        - key_positives: List of positive indicators
        - risks: List of identified risks
        - future_outlook: Growth potential assessment

    Raises:
        ValueError: If analysis fails
        APIError: If OpenAI API call fails
    """

    analysis_prompt = f"""You are a financial analyst helping beginners understand company financial reports.

Analyze this financial report excerpt and provide insights in simple, beginner-friendly language.

Return ONLY valid JSON (no markdown, no explanations) with this exact structure:
{{
    "company_summary": "A 2-3 sentence summary of what the company does and its financial health",
    "key_positives": [
        "Positive indicator or achievement 1",
        "Positive indicator or achievement 2",
        "Positive indicator or achievement 3"
    ],
    "risks": [
        "Risk or concern 1",
        "Risk or concern 2",
        "Risk or concern 3"
    ],
    "future_outlook": "1-2 sentence outlook on the company's growth potential"
}}

Financial Report Text:
{text}

Remember to:
- Use simple language suitable for beginners
- Focus on what matters for investment decisions
- If information is unclear, make reasonable inferences
- Always return valid JSON only"""

    try:
        client = get_openai_client()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful financial analyst explaining reports to beginners. Always respond with valid JSON only, no other text."
                },
                {
                    "role": "user",
                    "content": analysis_prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000,
            timeout=30
        )

        response_text = response.choices[0].message.content.strip()

        # Parse JSON response
        try:
            analysis = json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON if it's wrapped in markdown code blocks
            json_match = re.search(r'```(?:json)?\n?(.*?)\n?```', response_text, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group(1))
            else:
                # Try to find JSON object directly
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                else:
                    raise ValueError("Could not parse AI response as JSON")

        # Validate structure
        required_keys = ["company_summary", "key_positives", "risks", "future_outlook"]
        if not all(key in analysis for key in required_keys):
            raise ValueError("AI response missing required fields")

        # Ensure lists are lists
        if not isinstance(analysis["key_positives"], list):
            analysis["key_positives"] = [str(analysis["key_positives"])]
        if not isinstance(analysis["risks"], list):
            analysis["risks"] = [str(analysis["risks"])]

        # Limit to 5 items per list
        analysis["key_positives"] = analysis["key_positives"][:5]
        analysis["risks"] = analysis["risks"][:5]

        return analysis

    except APIError as e:
        raise ValueError(f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error analyzing report: {str(e)}")


def create_fallback_analysis(text: str) -> Dict[str, Any]:
    """
    Create a fallback analysis if AI fails.
    This provides basic structure without requiring API calls (for testing).

    Args:
        text: Extracted text from PDF

    Returns:
        Dictionary with basic analysis structure
    """
    # Extract some basic info for fallback
    text_lower = text.lower()

    key_positives = []
    risks = []

    # Simple heuristics
    if "revenue" in text_lower and "increase" in text_lower:
        key_positives.append("Revenue growth demonstrated in financial reports")
    if "profit" in text_lower:
        key_positives.append("Company maintains profitability")
    if "market" in text_lower:
        key_positives.append("Strong market presence and operations")

    if "loss" in text_lower:
        risks.append("Recent losses noted in financial statements")
    if "debt" in text_lower:
        risks.append("Notable debt levels require monitoring")
    if "decline" in text_lower:
        risks.append("Declining metrics in certain areas")

    # Pad if needed
    while len(key_positives) < 3:
        key_positives.append("Financial metrics need further evaluation")
    while len(risks) < 3:
        risks.append("Market conditions require close monitoring")

    return {
        "company_summary": "Financial report analysis indicates a company with mixed signals that requires deeper analysis.",
        "key_positives": key_positives[:5],
        "risks": risks[:5],
        "future_outlook": "Growth prospects depend on execution and market conditions."
    }
