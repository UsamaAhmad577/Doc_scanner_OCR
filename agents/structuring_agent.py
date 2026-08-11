"""
agents/structuring_agent.py

Structuring Agent: takes corrected plain text and converts it into
structured JSON, inferring the document type (invoice, note, form, etc.)
and shaping the output accordingly.
"""

import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_client = None

STRUCTURING_PROMPT = """You are a document structuring assistant. You will be \
given cleaned text extracted from a scanned document. Your job:

1. Identify the likely document type (e.g. "invoice", "receipt", "form", \
"handwritten_note", "plain_text", "id_card", "table").
2. Extract the content into structured JSON fields appropriate for that \
document type. For plain text/notes with no clear structure, just return \
the text under a "content" field.
3. Do NOT invent data that isn't present in the text.

Return ONLY valid JSON in this exact shape, with no explanation or markdown \
formatting:
{{
  "document_type": "...",
  "fields": {{ ... }}
}}

Text to structure:
---
{corrected_text}
---

JSON output:"""


def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _client


def structure_text(corrected_text: str) -> dict:
    """
    Convert corrected OCR text into structured JSON.

    Args:
        corrected_text: clean text from the correction agent.

    Returns:
        A dict with "document_type" and "fields". Falls back to a
        plain-text shape if the LLM output isn't valid JSON.
    """
    if not corrected_text or not corrected_text.strip():
        return {"document_type": "unknown", "fields": {}}

    client = _get_client()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": STRUCTURING_PROMPT.format(corrected_text=corrected_text),
            }
        ],
        temperature=0.1,
        response_format={"type": "json_object"},  # asks Groq to guarantee valid JSON
    )

    raw_output = response.choices[0].message.content.strip()

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        # Fallback: don't crash the pipeline if the model ever returns
        # malformed JSON — degrade gracefully instead.
        return {"document_type": "plain_text", "fields": {"content": corrected_text}}