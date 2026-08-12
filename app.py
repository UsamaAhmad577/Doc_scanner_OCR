"""
app.py

Streamlit front-end for the agentic OCR pipeline.
Run locally with:  streamlit run app.py
"""

import json
import os
import tempfile

import streamlit as st
from PIL import Image

from agents.orchestrator import run_pipeline

st.set_page_config(page_title="Agentic OCR Tool", page_icon="🤖", layout="wide")

st.title("🤖 Agentic OCR Tool")
st.write(
    "Upload an image and watch it move through a multi-agent pipeline: "
    "**extraction → correction → structuring**, with an orchestrator that "
    "flags low-confidence results for review."
)

uploaded_file = st.file_uploader(
    "Upload an image", type=["png", "jpg", "jpeg"], accept_multiple_files=False
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # PaddleOCR's predict() needs a file path, so save the upload to a temp file.
    # Convert to RGB first: uploaded PNGs are often RGBA, and PaddleOCR's
    # detection model expects 3-channel input.
    fd, tmp_path = tempfile.mkstemp(suffix=".png")
    os.close(fd)  # close the handle immediately (Windows locks files if left open)
    image.convert("RGB").save(tmp_path)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(image, caption="Uploaded image", use_column_width=True)

    with st.spinner("Running agentic pipeline (extraction \u2192 correction \u2192 structuring)..."):
        try:
            result = run_pipeline(tmp_path)
        finally:
            os.unlink(tmp_path)  # always clean up the temp file

    with col2:
        if result["needs_review"]:
            st.warning(f"⚠️ {result['review_reason']}")
        else:
            st.success(f"✅ Extraction confidence: {result['confidence']}%")

        tab1, tab2, tab3 = st.tabs(["Structured", "Corrected Text", "Raw OCR"])

        with tab1:
            st.subheader(f"Document type: {result['structured'].get('document_type', 'unknown')}")
            st.json(result["structured"])
            st.download_button(
                "Download JSON",
                data=json.dumps(result["structured"], indent=2),
                file_name="structured_output.json",
                mime="application/json",
            )

        with tab2:
            st.text_area("Corrected text", result["corrected_text"], height=250)
            st.download_button(
                "Download corrected text",
                data=result["corrected_text"],
                file_name="corrected_text.txt",
                mime="text/plain",
            )

        with tab3:
            st.text_area("Raw OCR output (before correction)", result["raw_text"], height=250)
            st.caption(
                "This is what PaddleOCR extracted before the correction agent "
                "cleaned it up — useful for seeing exactly what the LLM agent fixed."
            )
else:
    st.info("👆 Upload an image to run it through the pipeline.")

st.divider()
st.caption("Built by Usama · Multi-agent OCR pipeline · Source on GitHub")