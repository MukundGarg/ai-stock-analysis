"""
Pattern Detector Module

Identifies chart patterns from analyzed chart data.
"""

from typing import Dict, Any, Tuple
import numpy as np


def detect_pattern(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detect chart patterns from analyzed data.

    Args:
        analysis_data: Output from chart_processor.analyze_chart()

    Returns:
        Dictionary with pattern information:
        - pattern: Name of detected pattern
        - signal: Bullish/Bearish/Neutral
        - confidence: Low/Medium/High
        - description: Explanation of pattern
    """

    if not analysis_data.get("success"):
        return {
            "pattern": "Analysis Failed",
            "signal": "Neutral",
            "confidence": "Low",
            "description": "Could not analyze the chart image. Please ensure it's a valid price chart."
        }

    # Extract analysis data
    trend_info = analysis_data.get("trend_analysis", {})
    peaks_valleys = analysis_data.get("peaks_valleys", {})
    statistics = analysis_data.get("statistics", {})

    # Calculate scores
    uptrend_score = trend_info.get("uptrend_score", 0)
    downtrend_score = trend_info.get("downtrend_score", 0)
    lines_detected = trend_info.get("lines_detected", 0)

    peaks_count = peaks_valleys.get("peaks_count", 0)
    valleys_count = peaks_valleys.get("valleys_count", 0)

    top_intensity = statistics.get("top_intensity", 0)
    middle_intensity = statistics.get("middle_intensity", 0)
    bottom_intensity = statistics.get("bottom_intensity", 0)
    contrast = statistics.get("overall_contrast", 0)

    # --- Pattern Detection Logic ---

    # 1. Double Top Pattern
    # Characteristics: Two peaks at similar heights, valley in between
    if peaks_count >= 2 and valleys_count >= 1 and lines_detected > 0:
        peak_height_variance = abs(top_intensity - middle_intensity)
        if peak_height_variance < 15 and downtrend_score > uptrend_score:
            confidence = calculate_confidence(
                peaks_count >= 2 and valleys_count >= 1,
                downtrend_score > uptrend_score,
                lines_detected > 3
            )
            return {
                "pattern": "Double Top",
                "signal": "Bearish",
                "confidence": confidence,
                "description": "A double top pattern suggests potential downward reversal. Two peaks at similar levels indicate seller resistance. Watch for breakdown below the valley for confirmation."
            }

    # 2. Double Bottom Pattern
    # Characteristics: Two valleys at similar lows, peak in between
    if valleys_count >= 2 and peaks_count >= 1:
        valley_depth = abs(bottom_intensity - middle_intensity)
        if valley_depth < 15 and uptrend_score > downtrend_score:
            confidence = calculate_confidence(
                valleys_count >= 2 and peaks_count >= 1,
                uptrend_score > downtrend_score,
                lines_detected > 3
            )
            return {
                "pattern": "Double Bottom",
                "signal": "Bullish",
                "confidence": confidence,
                "description": "A double bottom pattern indicates potential upward reversal. Two lows at similar levels suggest buyer support. Break above the peak for bullish confirmation."
            }

    # 3. Uptrend Pattern
    # Characteristics: Higher lows and higher highs
    if uptrend_score > downtrend_score and valleys_count > 0:
        trend_strength = (uptrend_score - downtrend_score) / max(lines_detected, 1)
        if trend_strength > 0.3:
            confidence = calculate_confidence(
                uptrend_score > downtrend_score * 1.5,
                valleys_count > peaks_count,
                trend_strength > 0.5
            )
            return {
                "pattern": "Uptrend",
                "signal": "Bullish",
                "confidence": confidence,
                "description": "Strong uptrend pattern detected. Price is making higher highs and higher lows. Momentum appears positive. Consider buying strategies on pullbacks."
            }

    # 4. Downtrend Pattern
    # Characteristics: Lower highs and lower lows
    if downtrend_score > uptrend_score and peaks_count > 0:
        trend_strength = (downtrend_score - uptrend_score) / max(lines_detected, 1)
        if trend_strength > 0.3:
            confidence = calculate_confidence(
                downtrend_score > uptrend_score * 1.5,
                peaks_count > valleys_count,
                trend_strength > 0.5
            )
            return {
                "pattern": "Downtrend",
                "signal": "Bearish",
                "confidence": confidence,
                "description": "Strong downtrend pattern identified. Price is making lower highs and lower lows. Negative momentum visible. Exercise caution with long positions."
            }

    # 5. Head and Shoulders Pattern (simplified - one peak taller than neighbors)
    peak_positions = peaks_valleys.get("peak_positions", [])
    valley_positions = peaks_valleys.get("valley_positions", [])

    if len(peak_positions) >= 3:
        # Check if middle peak is tallest (head higher than shoulders)
        try:
            middle_idx = len(peak_positions) // 2
            if peak_count_at_position(peak_positions, middle_idx) > \
               peak_count_at_position(peak_positions, middle_idx - 1) and \
               peak_count_at_position(peak_positions, middle_idx) > \
               peak_count_at_position(peak_positions, middle_idx + 1):
                return {
                    "pattern": "Head and Shoulders",
                    "signal": "Bearish",
                    "confidence": "Medium",
                    "description": "Head and Shoulders reversal pattern detected. A tall middle peak with lower peaks on sides suggests bearish reversal. Neckline break could validate."
                }
        except:
            pass

    # 6. Triangle Pattern (consolidation)
    # Characteristics: Converging trend lines (narrowing price range)
    if lines_detected > 3 and contrast < 50 and (peaks_count > 0 and valleys_count > 0):
        if abs(peaks_count - valleys_count) <= 1:
            confidence = calculate_confidence(
                lines_detected > 5,
                contrast < 30,
                True
            )
            return {
                "pattern": "Triangle",
                "signal": "Neutral",
                "confidence": confidence,
                "description": "Triangle consolidation pattern identified. Price is in a narrowing range with converging support and resistance. Breakout coming soon above or below."
            }

    # 7. Wedge Pattern (upward or downward wedge)
    if lines_detected > 2 and contrast > 40:
        if uptrend_score > downtrend_score:
            return {
                "pattern": "Ascending Wedge",
                "signal": "Bearish",
                "confidence": "Medium",
                "description": "Ascending wedge pattern (bearish reversal). Price rises but in a narrowing range. Reversal likely when upper line is broken. Prepare for downside."
            }
        elif downtrend_score > uptrend_score:
            return {
                "pattern": "Descending Wedge",
                "signal": "Bullish",
                "confidence": "Medium",
                "description": "Descending wedge pattern (bullish reversal). Price falls but in a narrowing range. Reversal expected when lower line is broken. Prepare for upside."
            }

    # 8. Flag Pattern
    if lines_detected > 0 and valleys_count >= 2:
        return {
            "pattern": "Flag",
            "signal": "Neutral",
            "confidence": "Low",
            "description": "Possible flag consolidation pattern. Short pause in trend before continuation. Breakout direction will determine next move."
        }

    # Default: Neutral/No Clear Pattern
    return {
        "pattern": "No Clear Pattern",
        "signal": "Neutral",
        "confidence": "Low",
        "description": "Chart shows mixed signals with no dominant pattern. Continue monitoring for clearer technical setup before making trading decisions."
    }


def calculate_confidence(
    condition1: bool,
    condition2: bool,
    condition3: bool
) -> str:
    """
    Calculate confidence level based on met conditions.

    Args:
        condition1: Primary pattern condition
        condition2: Secondary pattern condition
        condition3: Tertiary pattern condition

    Returns:
        Confidence level: High/Medium/Low
    """
    met_conditions = sum([condition1, condition2, condition3])

    if met_conditions >= 3:
        return "High"
    elif met_conditions == 2:
        return "Medium"
    else:
        return "Low"


def peak_count_at_position(positions: list, index: int) -> int:
    """
    Safe peak count at position.

    Args:
        positions: List of positions
        index: Index to check

    Returns:
        Position count at index (or 0 if out of bounds)
    """
    try:
        return len([p for p in positions if p == index])
    except:
        return 0
