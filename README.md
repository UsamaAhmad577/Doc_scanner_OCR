# 📄 Simple OCR Tool

A lightweight OCR web app: upload an image, get the extracted text back, download it as `.txt`.
Built as Phase 1 of a larger project — a future phase turns this into a multi-agent
document-understanding pipeline (see [Roadmap](#roadmap) below).

**Live demo:** _add your Hugging Face Space / Streamlit Cloud link here once deployed_

![screenshot placeholder](docs/screenshot.png)

## Features
- Upload JPG/PNG images
- OpenCV preprocessing (grayscale, denoising, adaptive thresholding) for better accuracy on
  low-quality or unevenly-lit scans
- Confidence score estimate per extraction
- Download extracted text as `.txt`
- CI pipeline: lint + automated tests on every push/PR

## Tech stack
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) via `pytesseract`
- OpenCV for image preprocessing
- Streamlit for the UI
- GitHub Actions for CI

## Running locally

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/simple-ocr-tool.git
cd simple-ocr-tool

# 2. Install the Tesseract binary (Linux/Debian)
sudo apt-get install tesseract-ocr

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## Running tests

```bash
python tests/generate_fixture.py   # creates a synthetic sample image with known text
pytest tests/ -v
```

## Deployment (free)

### Option A: Hugging Face Spaces (recommended)
1. Create a new Space → SDK: **Streamlit**.
2. Connect it to this GitHub repo (or push directly to the Space's own git remote).
3. Hugging Face automatically reads `requirements.txt` **and** `packages.txt`
   (this repo includes both — `packages.txt` installs the `tesseract-ocr` system binary).
4. Every push to `main` triggers an automatic redeploy.

### Option B: Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io), connect your GitHub account.
2. Pick this repo, branch `main`, main file `app.py`.
3. Streamlit Cloud also reads `packages.txt` for apt-level dependencies.
4. Deploys automatically on every push to `main`.

Both are free; apps sleep after a period of inactivity and wake up on the next visit.

## Project structure
```
ocr-app/
├── app.py                      # Streamlit UI
├── ocr_engine.py                # OCR + preprocessing logic (testable, UI-independent)
├── requirements.txt
├── packages.txt                 # apt-level dependency: tesseract-ocr
├── tests/
│   ├── generate_fixture.py      # builds a synthetic test image
│   └── test_ocr.py
└── .github/workflows/ci.yml     # lint + test on every push/PR
```

## Roadmap
- [x] Phase 1 — simple OCR tool, CI pipeline, free deployment
- [ ] Phase 2 — agentic pipeline: extraction agent, LLM-based correction agent,
      structuring agent, orchestrator that routes by document type
- [ ] Phase 3 — support for multi-page PDFs and handwritten text

## License
MIT
