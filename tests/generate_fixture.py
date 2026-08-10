"""
Generates a simple synthetic image containing known text, so tests don't
depend on any external/downloaded sample image.
Run once: python tests/generate_fixture.py
"""

import os

from PIL import Image, ImageDraw, ImageFont

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
os.makedirs(FIXTURE_DIR, exist_ok=True)


def make_fixture():
    img = Image.new("RGB", (500, 150), color="white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32
        )
    except OSError:
        font = ImageFont.load_default()

    draw.text((20, 50), "HELLO WORLD 123", fill="black", font=font)
    img.save(os.path.join(FIXTURE_DIR, "sample_text.png"))


if __name__ == "__main__":
    make_fixture()
    print("Fixture generated.")
