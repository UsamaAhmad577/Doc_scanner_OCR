# 🤖 Agentic OCR Tool

An OCR web app that started simple and is being built up into a multi-agent
document-understanding pipeline — built as a learning + portfolio project,
documented honestly as it evolves.

**Live demo:** _add your Hugging Face Space link here once deployed_

## What it does

Upload an image → the pipeline extracts text, corrects OCR errors using an
LLM agent, and structures the result into JSON — with a routing decision
made by an orchestrator based on extraction confidence.

## Architecture

```
Upload → Orchestrator Agent
              │
              ▼
       Extraction Agent (PaddleOCR)
              │
              ▼
       Correction Agent (Groq LLM) ── fixes OCR typos using context
              │
              ▼
       Structuring Agent (Groq LLM) ── turns text into structured JSON
              │
              ▼
        Structured output + confidence flag
```

## Status

- [x] **Phase 1** — simple OCR tool (Tesseract), deployed with CI
- [x] **Phase 2 (core)** — agentic pipeline: extraction, correction,
      structuring, and orchestrator agents, all tested individually and
      end-to-end
- [ ] **In progress** — VLM fallback agent (built, not yet wired into the
      orchestrator's routing logic) for documents where PaddleOCR's
      detection fails entirely
- [ ] **Known limitation** — dense numeric tables (e.g. mark sheets, grids)
      have low detection recall with the current lightweight detection
      model; larger/server detection model under evaluation
- [ ] **Known limitation** — cursive handwriting is not detected by the
      default PaddleOCR pipeline (detection model trained primarily on
      printed/scene text); this is the specific problem the VLM fallback
      agent is being built to solve

## Tech stack

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) (PP-OCRv4) for text extraction
- [Groq API](https://console.groq.com) (`openai/gpt-oss-120b`) for correction and structuring agents
- Groq vision models (`qwen/qwen3.6-27b`) for the in-progress VLM fallback path
- Streamlit for the UI
- GitHub Actions for CI

## Running locally

```bash
git clone https://github.com/<your-username>/simple-ocr-tool.git
cd simple-ocr-tool

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

Install Tesseract (legacy Phase 1 path, still used as a fallback engine)
and Tesseract's system binary isn't required for the agentic pipeline itself
— PaddleOCR handles extraction. On Windows, PaddlePaddle installs via pip
directly, no extra system install needed.

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_key_here
```

Run it:
```bash
streamlit run app.py
```

## Running tests

```bash
python tests/generate_fixture.py
pytest tests/ -v
```

## Deployment (free — Hugging Face Spaces)

See the deployment steps in the project docs / commit history for the exact
Space configuration. Summary: SDK = Streamlit, `GROQ_API_KEY` set as a Space
secret (never committed), `requirements.txt` + `packages.txt` handle
dependencies automatically.

## Project structure
```
ocr-app/
├── app.py                          # Streamlit UI (agentic pipeline)
├── ocr_engine.py                   # Phase 1: simple Tesseract-based OCR
├── agents/
│   ├── extraction_agent.py         # PaddleOCR extraction
│   ├── correction_agent.py         # Groq LLM error correction
│   ├── structuring_agent.py        # Groq LLM → structured JSON
│   ├── vlm_extraction_agent.py     # Vision-LLM fallback (in progress)
│   └── orchestrator.py             # Coordinates the pipeline + routing
├── requirements.txt
├── packages.txt                    # apt-level deps for hosting
├── tests/
└── .github/workflows/ci.yml
```

## Roadmap
- [ ] Wire VLM fallback into orchestrator (auto-route when detection confidence is low/zero)
- [ ] Improve table/grid detection recall (larger detection model or table-specific pipeline)
- [ ] Multi-page PDF support

## License
MIT