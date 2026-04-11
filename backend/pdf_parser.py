"""
PDF Parser Module

Extracts text from PDF files for financial report analysis.
"""

import pdfplumber
from typing import Tuple


def extract_text_from_pdf(file_path: str) -> Tuple[str, str]:
    """
    Extract text from a PDF file.

    Args:
        file_path: Path to the PDF file

    Returns:
        Tuple of (extracted_text, filename)

    Raises:
        ValueError: If PDF cannot be read or is empty
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            if len(pdf.pages) == 0:
                raise ValueError("PDF file is empty")

            # Extract text from all pages
            text_content = []
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
                except Exception as e:
                    print(f"Warning: Could not extract text from page {page_num}: {str(e)}")

            if not text_content:
                raise ValueError("No text could be extracted from the PDF")

            full_text = "\n\n".join(text_content)
            return full_text, file_path

    except pdfplumber.exceptions.InvalidPDF:
        raise ValueError("Invalid PDF file. Please ensure the file is a valid PDF.")
    except FileNotFoundError:
        raise ValueError("PDF file not found.")
    except Exception as e:
        raise ValueError(f"Error reading PDF: {str(e)}")


def clean_and_truncate_text(text: str, max_length: int = 8000) -> str:
    """
    Clean and truncate extracted text for LLM processing.

    Args:
        text: Raw extracted text
        max_length: Maximum length of text to keep (in characters)

    Returns:
        Cleaned and truncated text
    """
    # Remove extra whitespace and normalize
    cleaned = " ".join(text.split())

    # Truncate to max length
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length] + "..."

    return cleaned


def get_pdf_metadata(file_path: str) -> dict:
    """
    Extract metadata from PDF.

    Args:
        file_path: Path to the PDF file

    Returns:
        Dictionary with metadata
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            return {
                "total_pages": len(pdf.pages),
                "has_metadata": pdf.metadata is not None,
                "metadata": pdf.metadata or {}
            }
    except Exception as e:
        return {
            "error": str(e),
            "total_pages": 0
        }
