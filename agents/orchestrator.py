"""
agents/orchestrator.py

Orchestrator Agent: coordinates the full pipeline — extraction, correction,
structuring — and makes a routing decision based on OCR confidence.
This is the single entry point the UI calls.
"""

from agents.correction_agent import correct_text
from agents.extraction_agent import extract_text
from agents.structuring_agent import structure_text

LOW_CONFIDENCE_THRESHOLD = 60.0  # below this, we flag the result for human review


def run_pipeline(image_path: str) -> dict:
    """
    Run the full agentic OCR pipeline on an image.

    Args:
        image_path: path to the image file on disk.

    Returns:
        dict containing the output of every stage, so the UI can show
        the full pipeline (not just the final result) — useful both for
        transparency and for debugging.
    """
    # Stage 1: Extraction
    extraction_result = extract_text(image_path)
    raw_text = extraction_result["text"]
    avg_confidence = extraction_result["avg_confidence"]

    needs_review = avg_confidence < LOW_CONFIDENCE_THRESHOLD or not raw_text.strip()

    if not raw_text.strip():
        # Nothing was detected at all — no point calling the LLM agents.
        return {
            "raw_text": "",
            "corrected_text": "",
            "structured": {"document_type": "unknown", "fields": {}},
            "confidence": avg_confidence,
            "needs_review": True,
            "review_reason": "No text detected in the image.",
        }

    # Stage 2: Correction
    corrected_text = correct_text(raw_text)

    # Stage 3: Structuring
    structured = structure_text(corrected_text)

    return {
        "raw_text": raw_text,
        "corrected_text": corrected_text,
        "structured": structured,
        "confidence": avg_confidence,
        "needs_review": needs_review,
        "review_reason": (
            f"Low OCR confidence ({avg_confidence}%) — verify manually."
            if needs_review
            else None
        ),
    }