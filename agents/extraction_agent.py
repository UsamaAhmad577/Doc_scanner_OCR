"""
agents/extraction_agent.py

Extraction Agent: runs OCR using PaddleOCR and returns raw extracted text
plus per-line confidence scores. This is the foundation the other agents
build on top of.
"""

from paddleocr import PaddleOCR

_ocr_engine = None


def _get_engine():
    global _ocr_engine
    if _ocr_engine is None:
        _ocr_engine = PaddleOCR(lang="en", ocr_version="PP-OCRv4")
    return _ocr_engine


def extract_text(image_path: str) -> dict:
    """
    Run OCR on an image file and return structured results.

    Args:
        image_path: path to an image file on disk.

    Returns:
        dict with:
          - text: all detected text joined by newlines
          - lines: list of {"text": ..., "confidence": ...} per detected line
          - avg_confidence: overall average confidence (0-100)
    """
    ocr = _get_engine()
    result = ocr.predict(image_path)

    if not result:
        return {"text": "", "lines": [], "avg_confidence": 0.0}

    res = result[0]
    texts = res.get("rec_texts", [])
    scores = res.get("rec_scores", [])

    full_text = "\n".join(texts)
    avg_confidence = round(sum(scores) / len(scores) * 100, 2) if scores else 0.0

    lines = [
        {"text": t, "confidence": round(s * 100, 2)}
        for t, s in zip(texts, scores)
    ]

    return {"text": full_text, "lines": lines, "avg_confidence": avg_confidence}