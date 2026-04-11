"""
Chart Image Processor Module

Processes chart images to extract technical features for pattern detection.
"""

import cv2
import numpy as np
from PIL import Image
import io
from typing import Tuple, Dict, Any


def load_image_from_bytes(image_bytes: bytes) -> np.ndarray:
    """
    Load image from bytes and convert to OpenCV format.

    Args:
        image_bytes: Binary image data

    Returns:
        Image as numpy array (BGR format)

    Raises:
        ValueError: If image cannot be loaded
    """
    try:
        # Convert bytes to PIL Image
        pil_image = Image.open(io.BytesIO(image_bytes))

        # Convert RGBA to RGB if needed
        if pil_image.mode == 'RGBA':
            pil_image = pil_image.convert('RGB')

        # Convert PIL to numpy array and BGR for OpenCV
        image_array = np.array(pil_image)
        image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        return image_array
    except Exception as e:
        raise ValueError(f"Could not load image: {str(e)}")


def preprocess_image(image: np.ndarray) -> np.ndarray:
    """
    Preprocess image for analysis.

    Args:
        image: Input image (BGR)

    Returns:
        Preprocessed grayscale image
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    # This helps with contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(blurred)

    return enhanced


def detect_edges(image: np.ndarray) -> np.ndarray:
    """
    Detect edges in image using Canny edge detection.

    Args:
        image: Preprocessed grayscale image

    Returns:
        Edge-detected image
    """
    # Apply Canny edge detection
    edges = cv2.Canny(image, 50, 150)

    return edges


def detect_trend_lines(image: np.ndarray) -> Dict[str, Any]:
    """
    Detect trend lines in the chart image using Hough line detection.

    Args:
        image: Preprocessed image

    Returns:
        Dictionary with trend line information
    """
    edges = detect_edges(image)

    # Detect lines using Hough Line Transform
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=50,
        minLineLength=50,
        maxLineGap=10
    )

    trend_info = {
        "lines_detected": 0,
        "uptrend_score": 0,
        "downtrend_score": 0,
        "slope_angles": []
    }

    if lines is not None:
        trend_info["lines_detected"] = len(lines)

        # Analyze slopes to determine trend direction
        for line in lines:
            x1, y1, x2, y2 = line[0]

            # Calculate slope and angle
            if x2 - x1 != 0:
                slope = (y2 - y1) / (x2 - x1)
                angle = np.arctan(slope) * 180 / np.pi

                trend_info["slope_angles"].append(angle)

                # Positive angle (upward slope) = uptrend
                if angle > 5:
                    trend_info["uptrend_score"] += 1
                # Negative angle (downward slope) = downtrend
                elif angle < -5:
                    trend_info["downtrend_score"] += 1

    return trend_info


def detect_peaks_and_valleys(image: np.ndarray, window_size: int = 20) -> Dict[str, Any]:
    """
    Detect peaks and valleys in the chart (potential reversal points).

    Args:
        image: Preprocessed image
        window_size: Window size for peak/valley detection

    Returns:
        Dictionary with peak and valley information
    """
    # Get vertical projection (sum of pixel values in each column)
    vertical_projection = np.sum(image, axis=0)

    # Normalize
    if vertical_projection.max() > 0:
        vertical_projection = vertical_projection / vertical_projection.max()

    peaks = []
    valleys = []

    # Detect peaks and valleys
    for i in range(window_size, len(vertical_projection) - window_size):
        window = vertical_projection[i - window_size:i + window_size]

        # Peak: local maximum
        if vertical_projection[i] == window.max() and vertical_projection[i] > 0.5:
            peaks.append(i)

        # Valley: local minimum
        if vertical_projection[i] == window.min() and vertical_projection[i] < 0.5:
            valleys.append(i)

    return {
        "peaks_count": len(peaks),
        "valleys_count": len(valleys),
        "peak_positions": peaks,
        "valley_positions": valleys
    }


def get_chart_statistics(image: np.ndarray) -> Dict[str, Any]:
    """
    Calculate statistics about the chart.

    Args:
        image: Preprocessed image

    Returns:
        Dictionary with statistical information
    """
    height, width = image.shape

    # Divide chart into regions (top/bottom for highs/lows)
    top_third = image[:height // 3, :]
    bottom_third = image[2 * height // 3:, :]
    middle_third = image[height // 3:2 * height // 3, :]

    return {
        "image_height": height,
        "image_width": width,
        "top_intensity": np.mean(top_third),
        "middle_intensity": np.mean(middle_third),
        "bottom_intensity": np.mean(bottom_third),
        "overall_contrast": np.std(image)
    }


def analyze_chart(image_bytes: bytes) -> Dict[str, Any]:
    """
    Comprehensive chart analysis.

    Args:
        image_bytes: Binary image data

    Returns:
        Dictionary with complete analysis
    """
    try:
        # Load and preprocess
        image = load_image_from_bytes(image_bytes)
        preprocessed = preprocess_image(image)

        # Perform multiple analyses
        trend_info = detect_trend_lines(preprocessed)
        peaks_valleys = detect_peaks_and_valleys(preprocessed)
        statistics = get_chart_statistics(preprocessed)

        return {
            "success": True,
            "trend_analysis": trend_info,
            "peaks_valleys": peaks_valleys,
            "statistics": statistics,
            "image_shape": preprocessed.shape
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
