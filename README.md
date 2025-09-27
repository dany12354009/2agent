# DuoForge (2-agent code lab)

DuoForge is a FastAPI-based web platform where two AI agents collaborate to transform a user specification into production-ready code. The system runs an architect/coder/reviewer workflow, tracks a working directory on disk, and packages the resulting project for download.

## Features
- **FastAPI + WebSockets** backend that orchestrates sessions and streams agent events to the browser.
- **Architect, Coder, Reviewer** agents using the same base LLM with distinct prompts.
- **Workspace manager** capable of listing files, applying file-level or patch-level edits, generating README documentation, and exporting zip archives.
- **Safety filter** that blocks obviously malicious build requests.
- **Minimal frontend** that captures user specifications, displays the streaming debate, and provides a download link once ready.

## Running locally
1. Create and populate a Python 3.10+ virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and fill in your OpenAI credentials.
4. Start the server: `uvicorn server.main:app --reload`.
5. Open `http://localhost:8000/` in a browser.

## Testing
Run the automated tests with `pytest`.

## Project layout
```
server/
  agents.py         # Agent system prompts and payload helpers
  llm.py            # Async OpenAI chat client wrapper
  orchestrator.py   # Agent turn loop and session orchestration
  repo.py           # Workspace manager for snapshot/apply/zip/README
  main.py           # FastAPI application and WebSocket handling
  static/           # Frontend assets served by FastAPI
requirements.txt
```
