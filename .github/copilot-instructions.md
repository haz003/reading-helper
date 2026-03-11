# AI Coding Agent Instructions for Reading Helper

These instructions help AI coding agents (Copilot-style) work productively in this repository.

## Quick Context
- Project language: Python (backend uses FastAPI). See [backend/main.py](backend/main.py).
- Core files: [backend/word_analyzer.py](backend/word_analyzer.py), [backend/dictionary_service.py](backend/dictionary_service.py), [backend/requirements.txt](backend/requirements.txt).
- Docs: [docs/SETUP.md](docs/SETUP.md) and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) contain onboarding and architecture notes.

## What to do first
- Run the Setup steps in docs/SETUP.md to reproduce the dev environment (venv + `pip install -r requirements.txt`).
- Start the backend locally with: `cd backend && uvicorn main:app --reload`.

## Code Style & Conventions
- Follow existing Python style in the repo: PEP8-like formatting, docstrings for public functions, and clear variable names. See `backend/main.py` and `backend/word_analyzer.py` for examples.
- Prefer small, focused functions. Keep I/O (HTTP endpoints) separate from business logic (`word_analyzer.py`).

## Architecture Notes
- Backend: FastAPI app exposes `/process-text` (file upload) and `/test-text` (raw text) endpoints in `backend/main.py`.
- Text processing lives in `backend/word_analyzer.py`. Definitions are fetched via `backend/dictionary_service.py`.
- The frontend (if present) will POST files to `/process-text`; return shape must stay compatible with current endpoints.

## Build / Run / Test Commands
- Create venv and install deps (Windows PowerShell):

  cd backend
  python -m venv venv
  venv\Scripts\Activate.ps1
  pip install -r requirements.txt

- Run server:

  uvicorn main:app --reload

## Repository Conventions
- Do not commit `venv/`, `.env`, or `__pycache__` — follow `docs/SETUP.md`.
- When modifying `word_analyzer.py`, preserve tokenization behavior: tokens preserve punctuation and return a list of objects with keys `word`, `is_hard`, and `definition`.

## Integration & External Dependencies
- `wordfreq` is used for frequency heuristics; `requests` may be used in `dictionary_service.py` to fetch definitions. Use `backend/requirements.txt` to manage versions.

## Security & Operational Notes
- CORS in `backend/main.py` is permissive (`allow_origins=["*"]`) — restrict this in production.
- Secrets (API keys) should go in a `.env` file or secure vault. Do NOT commit secrets.

## When to Ask for Clarification
- If a proposed change alters the public API shape (response fields, endpoint names), ask before merging.
- If a new dependency is needed, propose it and explain why; do not add dependencies without approval.

## Editing & Pull Request Guidance
- Keep PRs small and focused. Reference relevant docs (link to `docs/ARCHITECTURE.md` or `docs/PHASE_GUIDE.md`).
- Include a brief manual test plan for backend changes (example input and expected output for `analyze_text`).

If any of this is unclear or you want conventions extended (linting, CI, tests), tell me and I'll update this file.
