"""
app.py

Streamlit front-end for the OCR tool.
Run locally with:  streamlit run app.py
"""

import io

import streamlit as st
from PIL import Image

from ocr_engine import extract_text_with_confidence

st.set_page_config(page_title="Simple OCR Tool", page_icon="📄", layout="centered")

st.title("📄 Simple OCR Tool")
st.write(
    "Upload an image (JPG/PNG) and extract the text inside it. "
    "Built with Tesseract OCR + OpenCV preprocessing."
)

uploaded_file = st.file_uploader(
    "Upload an image", type=["png", "jpg", "jpeg"], accept_multiple_files=False
)

with st.sidebar:
    st.header("Options")
    lang = st.selectbox(
        "Language",
        options=["eng", "eng+urd", "eng+ara"],
        help="Tesseract language pack to use. More packs can be added in requirements.",
    )
    st.caption(
        "Note: only 'eng' is guaranteed to work out of the box on the free "
        "hosting tiers unless the extra language data is installed."
    )

if uploaded_file is not None:
    image_bytes = uploaded_file.read()
    image = Image.open(io.BytesIO(image_bytes))

    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Uploaded image", use_container_width=True)

    with st.spinner("Extracting text..."):
        result = extract_text_with_confidence(image, lang=lang)

    with col2:
        st.subheader("Extracted text")
        if result["text"]:
            st.text_area("Result", result["text"], height=300)
            st.caption(f"Estimated OCR confidence: {result['avg_confidence']}%")
            st.download_button(
                label="Download as .txt",
                data=result["text"],
                file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_extracted.txt",
                mime="text/plain",
            )
        else:
            st.warning(
                "No text was detected. Try a clearer image or a different scan."
            )
else:
    st.info("👆 Upload an image to get started.")

st.divider()
st.caption("Built by Usama · Source on GitHub")
