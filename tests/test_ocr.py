import os
import sys

from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ocr_engine import extract_text, extract_text_with_confidence  # noqa: E402

FIXTURE_PATH = os.path.join(
    os.path.dirname(__file__), "fixtures", "sample_text.png"
)


def test_fixture_exists():
    assert os.path.exists(FIXTURE_PATH), (
        "Run `python tests/generate_fixture.py` before testing."
    )


def test_extract_text_returns_expected_words():
    image = Image.open(FIXTURE_PATH)
    text = extract_text(image, preprocess=True)
    assert "HELLO" in text.upper()
    assert "WORLD" in text.upper()


def test_extract_text_without_preprocessing():
    image = Image.open(FIXTURE_PATH)
    text = extract_text(image, preprocess=False)
    assert "HELLO" in text.upper()


def test_extract_text_with_confidence_structure():
    image = Image.open(FIXTURE_PATH)
    result = extract_text_with_confidence(image)
    assert "text" in result
    assert "avg_confidence" in result
    assert isinstance(result["avg_confidence"], float)
    assert result["avg_confidence"] >= 0


def test_blank_image_returns_empty_or_near_empty():
    blank = Image.new("RGB", (200, 100), color="white")
    text = extract_text(blank)
    assert text.strip() == "" or len(text.strip()) < 5
