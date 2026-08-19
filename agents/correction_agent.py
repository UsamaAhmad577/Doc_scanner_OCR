"""
agents/correction_agent.py

Correction Agent: takes raw OCR output and asks an LLM to fix obvious
recognition errors (dropped/swapped characters, broken words) using
surrounding context, without inventing new content.
"""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_client = None

CORRECTION_PROMPT = """You are an OCR correction assistant. You will be given \
raw text extracted from an image by an OCR engine. The OCR engine sometimes \
drops or misreads characters (e.g. "ELLO" instead of "HELLO").

Your job: fix obvious OCR recognition errors using context, WITHOUT adding \
any new information, sentences, or content that wasn't implied by the \
original text. If a word looks intentionally unusual, leave it as is rather \
than guessing.

Return ONLY the corrected text, with no explanation, preamble, or commentary.

Raw OCR text:
---
{raw_text}
---

Corrected text:"""


def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _client


def correct_text(raw_text: str) -> str:
    """
    Send raw OCR text to the LLM for error correction.

    Args:
        raw_text: the raw text output from the extraction agent.

    Returns:
        Corrected text as a string. Falls back to the original text
        if the input is empty or the API call fails.
    """
    if not raw_text or not raw_text.strip():
        return raw_text

    client = _get_client()

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": CORRECTION_PROMPT.format(raw_text=raw_text)}
        ],
        temperature=0.1,  # low temperature: we want faithful correction, not creativity
    )

    return response.choices[0].message.content.strip()