"""
Pattern Detector Module — CV heuristics on chart images; used as fallback / helper to vision.
"""

from __future__ import annotations

from typing import Any


def _label_to_score(label: str) -> int:
    return {"High": 72, "Medium": 55, "Low": 38}.get(label, 40)


def _build_cv_extras(
    analysis_data: dict[str, Any],
    pattern: str,
    signal: str,
    confidence_label: str,
    description: str,
    reasoning: str,
) -> dict[str, Any]:
    peaks_valleys = analysis_data.get("peaks_valleys", {})
    stats = analysis_data.get("statistics", {})
    trend_info = analysis_data.get("trend_analysis", {})

    peaks = peaks_valleys.get("peak_positions", [])
    valleys = peaks_valleys.get("valley_positions", [])
    w = stats.get("image_width") or 0
    h = stats.get("image_height") or 0

    sr_parts = []
    if peaks:
        sr_parts.append(
            f"Multiple swing highs detected across the chart width (~{len(peaks)}); "
            "treat horizontal bands near those areas as potential resistance zones to confirm on price scale."
        )
    if valleys:
        sr_parts.append(
            f"Multiple swing lows (~{len(valleys)}); these columns may correspond to support tests "
            "(verify on actual price labels — image analysis is approximate)."
        )
    if not sr_parts:
        sr_parts.append(
            "Support/resistance are unclear from geometry alone; use exchange price levels and volume for confirmation."
        )

    line_n = trend_info.get("lines_detected", 0)
    upt = trend_info.get("uptrend_score", 0)
    dnt = trend_info.get("downtrend_score", 0)
    trendlines = (
        f"Detected {line_n} line segments from edges; upward segments ~{upt}, downward ~{dnt}. "
        "Slopes are noisy on screenshots — prefer drawing trendlines manually on the charting platform."
    )

    breakout = (
        "Breakout/breakdown cannot be confirmed from a static image without volume and closing levels; "
        "watch for closes beyond the range with participation."
    )

    candles = (
        "Candlestick patterns are not reliably parsed from this pipeline; use vision analysis or "
        "read candles directly in your charting app."
    )

    return {
        "pattern": pattern,
        "signal": signal,
        "confidence": confidence_label,
        "confidence_score": _label_to_score(confidence_label),
        "description": description,
        "reasoning": reasoning,
        "support_resistance": " ".join(sr_parts),
        "trendlines": trendlines,
        "breakout_notes": breakout,
        "candlestick_notes": candles,
        "beginner_explanation": description,
        "trade_setup": {
            "entry_zone": "Inferred from chart structure",
            "stop_loss_zone": "Approximate zone based on swing geometry",
            "target_1": "Estimated based on pattern projection",
            "target_2": "Projected from pattern structure",
            "risk_reward_ratio": "Estimated from structure",
        },
        "pattern_quality": {
            "purity_score": 50,
            "false_signal_risk": "Medium",
            "breakdown_continuation_probability": "Inferred from structure",
        },
        "market_context": {
            "current_trend": "Inferred from swing structure",
            "market_structure_alignment": "Inferred",
            "volatility_regime": "Inferred from candle density",
        },
        "confirmation": {
            "what_confirms": "Inferred from pattern structure",
            "what_invalidates": "Based on swing invalidation logic",
            "current_state": "Inferred (low confidence)",
        },
        "scenarios": {
            "bull_case": "Low confidence scenario modeling",
            "bear_case": "Low confidence scenario modeling",
            "neutral_case": "Low confidence scenario modeling",
        },
        "institutional_interpretation": {
            "institutional_action": "Inferred from structure",
            "liquidity_hunt_risk": "Possible stop hunt inferred",
            "dominant_behavior": "Inferred from structure",
        },
        "analysis_method": "cv_geometry",
        "chart_geometry": {"width": w, "height": h, "lines_detected": line_n},
    }


def detect_pattern(analysis_data: dict[str, Any]) -> dict[str, Any]:
    """
    Detect chart patterns from analyze_chart() output (geometry-based; approximate).
    """

    if not analysis_data.get("success"):
        return _build_cv_extras(
            analysis_data,
            "Analysis Failed",
            "Neutral",
            "Low",
            "Could not analyze the chart image. Please ensure it's a valid price chart screenshot.",
            "Image processing failed or returned no features.",
        )

    trend_info = analysis_data.get("trend_analysis", {})
    peaks_valleys = analysis_data.get("peaks_valleys", {})
    statistics = analysis_data.get("statistics", {})

    uptrend_score = trend_info.get("uptrend_score", 0)
    downtrend_score = trend_info.get("downtrend_score", 0)
    lines_detected = trend_info.get("lines_detected", 0)

    peaks_count = peaks_valleys.get("peaks_count", 0)
    valleys_count = peaks_valleys.get("valleys_count", 0)

    top_intensity = statistics.get("top_intensity", 0)
    middle_intensity = statistics.get("middle_intensity", 0)
    bottom_intensity = statistics.get("bottom_intensity", 0)
    contrast = statistics.get("overall_contrast", 0)

    peak_positions = peaks_valleys.get("peak_positions", [])
    peak_intensities = peaks_valleys.get("peak_intensities", [])
    valley_positions = peaks_valleys.get("valley_positions", [])
    valley_intensities = peaks_valleys.get("valley_intensities", [])

    def finalize(
        pattern: str,
        signal: str,
        conf_label: str,
        description: str,
        reasoning: str,
    ) -> dict[str, Any]:
        return _build_cv_extras(analysis_data, pattern, signal, conf_label, description, reasoning)

    # --- Head & shoulders: three peaks in x-order, middle highest intensity ---
    if len(peak_positions) >= 3 and len(peak_intensities) == len(peak_positions):
        pairs = sorted(zip(peak_positions, peak_intensities), key=lambda x: x[0])
        for i in range(len(pairs) - 2):
            left, mid, right = pairs[i], pairs[i + 1], pairs[i + 2]
            if mid[1] > left[1] and mid[1] > right[1] and mid[1] >= max(left[1], right[1]) * 0.92:
                conf = calculate_confidence(True, peaks_count >= 3, lines_detected > 2)
                desc = (
                    "Three swing highs appear with the middle one most prominent — similar to a head-and-shoulders "
                    "shape in price action. Traders watch for a break below the 'neckline' (the lows between peaks) "
                    "to validate a bearish reversal (educational only)."
                )
                reason = (
                    f"Ordered peaks at x≈{left[0]}, {mid[0]}, {right[0]} with middle column intensity highest "
                    f"({mid[1]:.2f} vs {left[1]:.2f}/{right[1]:.2f}). This is a geometric proxy, not a price-level H&S."
                )
                return finalize("Head and Shoulders", "Bearish", conf, desc, reason)

    # Double top
    if peaks_count >= 2 and valleys_count >= 1 and lines_detected > 0:
        peak_height_variance = abs(top_intensity - middle_intensity)
        if peak_height_variance < 15 and downtrend_score > uptrend_score:
            conf = calculate_confidence(
                peaks_count >= 2 and valleys_count >= 1,
                downtrend_score > uptrend_score,
                lines_detected > 3,
            )
            desc = (
                "Two prominent highs with selling pressure between them can form a double top — a bearish reversal "
                "idea if price later breaks below the intervening low (confirm on actual prices)."
            )
            reason = (
                f"Two+ peaks, valley between, downward-biased line slopes (down {downtrend_score} vs up {uptrend_score}). "
                f"Top/mid intensity gap small ({peak_height_variance:.1f}), suggesting similar 'high' bands in the image."
            )
            return finalize("Double Top", "Bearish", conf, desc, reason)

    # Double bottom
    if valleys_count >= 2 and peaks_count >= 1:
        valley_depth = abs(bottom_intensity - middle_intensity)
        if valley_depth < 15 and uptrend_score > downtrend_score:
            conf = calculate_confidence(
                valleys_count >= 2 and peaks_count >= 1,
                uptrend_score > downtrend_score,
                lines_detected > 3,
            )
            desc = (
                "Two similar lows with a bounce between can resemble a double bottom — often watched for bullish "
                "reversal if price breaks above the middle peak (confirm with volume)."
            )
            reason = (
                f"Two+ valleys, upward-biased slopes (up {uptrend_score} vs down {downtrend_score}). "
                f"Bottom/mid intensity gap {valley_depth:.1f} suggests comparable low zones in the raster."
            )
            return finalize("Double Bottom", "Bullish", conf, desc, reason)

    # Uptrend
    if uptrend_score > downtrend_score and valleys_count > 0:
        trend_strength = (uptrend_score - downtrend_score) / max(lines_detected, 1)
        if trend_strength > 0.3:
            conf = calculate_confidence(
                uptrend_score > downtrend_score * 1.5,
                valleys_count > peaks_count,
                trend_strength > 0.5,
            )
            desc = (
                "Geometry suggests higher lows / upward slopes — consistent with an uptrend narrative. "
                "Buy-the-dip ideas are beginner talk only; always define risk."
            )
            reason = (
                f"Uptrend score {uptrend_score} beats downtrend {downtrend_score}; trend_strength {trend_strength:.2f}; "
                f"{valleys_count} valley columns."
            )
            return finalize("Uptrend", "Bullish", conf, desc, reason)

    # Downtrend
    if downtrend_score > uptrend_score and peaks_count > 0:
        trend_strength = (downtrend_score - uptrend_score) / max(lines_detected, 1)
        if trend_strength > 0.3:
            conf = calculate_confidence(
                downtrend_score > uptrend_score * 1.5,
                peaks_count > valleys_count,
                trend_strength > 0.5,
            )
            desc = (
                "Geometry suggests lower highs / downward slopes — downtrend narrative. "
                "Avoid catching falling knives without a plan."
            )
            reason = (
                f"Downtrend score {downtrend_score} over uptrend {uptrend_score}; trend_strength {trend_strength:.2f}; "
                f"{peaks_count} peak columns."
            )
            return finalize("Downtrend", "Bearish", conf, desc, reason)

    # Triangle consolidation
    if lines_detected > 3 and contrast < 50 and peaks_count > 0 and valleys_count > 0:
        if abs(peaks_count - valleys_count) <= 1:
            conf = calculate_confidence(lines_detected > 5, contrast < 30, True)
            desc = (
                "Converging swings (triangle-style consolidation) mean volatility compression; "
                "breakout direction often matters more than the triangle label itself."
            )
            reason = f"Many lines ({lines_detected}), moderate contrast ({contrast:.1f}), balanced peaks/valleys."
            return finalize("Symmetrical Triangle", "Neutral", conf, desc, reason)

    # Wedges from slope imbalance
    if lines_detected > 2 and contrast > 40:
        if uptrend_score > downtrend_score:
            desc = (
                "Rising wedge (simplified): upward-sloping edges with narrowing range — often taught as bearish "
                "reversal risk; needs confirmation."
            )
            reason = f"More upward-sloped segments than down; contrast {contrast:.1f}."
            return finalize("Rising Wedge", "Bearish", "Medium", desc, reason)
        if downtrend_score > uptrend_score:
            desc = (
                "Falling wedge: downward-sloping narrowing range — often taught as bullish reversal candidate "
                "when broken upward."
            )
            reason = f"More downward-sloped segments; contrast {contrast:.1f}."
            return finalize("Falling Wedge", "Bullish", "Medium", desc, reason)

    desc = (
        "No dominant geometric pattern passed thresholds — the screenshot may be noisy, non-price, or multi-timeframe. "
        "Try a cleaner candlestick chart or use the AI vision result when available."
    )
    reason = (
        f"Peaks={peaks_count}, valleys={valleys_count}, lines={lines_detected}, "
        f"up/down scores {uptrend_score}/{downtrend_score}, contrast={contrast:.1f}."
    )
    return finalize("No clear pattern", "Neutral", "Low", desc, reason)


def calculate_confidence(condition1: bool, condition2: bool, condition3: bool) -> str:
    met = sum([condition1, condition2, condition3])
    if met >= 3:
        return "High"
    if met == 2:
        return "Medium"
    return "Low"
