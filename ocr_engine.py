"""
ocr_engine.py

Core OCR logic: image preprocessing + text extraction.
Kept separate from app.py so it can be unit-tested without Streamlit.
"""

import io
from typing import Union

import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image


def _pil_to_cv2(image: Image.Image) -> np.ndarray:
    """Convert a PIL image to an OpenCV (BGR) array."""
    rgb = np.array(image.convert("RGB"))
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)


def preprocess_image(image: Image.Image) -> np.ndarray:
    """
    Apply a standard preprocessing pipeline to improve OCR accuracy:
    grayscale -> denoise -> adaptive threshold.

    Returns a single-channel (binary) OpenCV image ready for Tesseract.
    """
    cv_img = _pil_to_cv2(image)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    # Light denoising helps with phone-camera noise without blurring text edges.
    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    # Adaptive threshold handles uneven lighting/shadows better than a global threshold.
    thresh = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=31,
        C=15,
    )
    return thresh


def extract_text(
    image: Union[Image.Image, bytes],
    lang: str = "eng",
    preprocess: bool = True,
) -> str:
    """
    Extract text from an image using Tesseract OCR.

    Args:
        image: A PIL Image, or raw image bytes.
        lang: Tesseract language code (default English).
        preprocess: Whether to run the preprocessing pipeline first.
                    Turn off for already-clean, high-contrast scans.

    Returns:
        Extracted text as a string (stripped of trailing whitespace).
    """
    if isinstance(image, bytes):
        image = Image.open(io.BytesIO(image))

    if preprocess:
        processed = preprocess_image(image)
        text = pytesseract.image_to_string(processed, lang=lang)
    else:
        text = pytesseract.image_to_string(image, lang=lang)

    return text.strip()


def extract_text_with_confidence(image: Image.Image, lang: str = "eng") -> dict:
    """
    Run OCR and also return a rough average confidence score, useful for
    flagging low-quality scans to the user in the UI.
    """
    processed = preprocess_image(image)
    data = pytesseract.image_to_data(
        processed, lang=lang, output_type=pytesseract.Output.DICT
    )

    confidences = [int(c) for c in data["conf"] if c != "-1" and int(c) >= 0]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    text = pytesseract.image_to_string(processed, lang=lang).strip()

    return {"text": text, "avg_confidence": round(avg_confidence, 2)}
