"""FastAPI application entry point for DuoForge."""

from __future__ import annotations

import json
import logging
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .orchestrator import Orchestrator
from .repo import RepoManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="DuoForge", version="1.0.0")

RUNS_ROOT = Path("runs")
RUNS_ROOT.mkdir(exist_ok=True)

MALICIOUS_KEYWORDS = {
    "malware",
    "virus",
    "ransomware",
    "botnet",
    "keylogger",
    "credential",
    "phishing",
    "exploit",
}


@dataclass
class SessionState:
    session_id: str
    repo: RepoManager


sessions: Dict[str, SessionState] = {}


@app.post("/api/sessions")
async def create_session() -> JSONResponse:
    session_id = uuid.uuid4().hex
    run_root = RUNS_ROOT / session_id
    repo = RepoManager(run_root)
    sessions[session_id] = SessionState(session_id, repo)
    return JSONResponse({"session_id": session_id})


@app.websocket("/ws/{session_id}")
async def websocket_handler(websocket: WebSocket, session_id: str) -> None:
    state = sessions.get(session_id)
    if state is None:
        await websocket.close(code=4404)
        return

    await websocket.accept()
    try:
        payload = await websocket.receive_text()
        message = json.loads(payload)
        spec = (message.get("prompt") or "").strip()
    except (json.JSONDecodeError, KeyError, TypeError):
        await websocket.send_text(json.dumps({"type": "error", "content": "Invalid payload."}))
        await websocket.close(code=1003)
        return
    except WebSocketDisconnect:
        return

    if not spec:
        await websocket.send_text(json.dumps({"type": "error", "content": "Specification required."}))
        await websocket.close()
        return

    if any(keyword in spec.lower() for keyword in MALICIOUS_KEYWORDS):
        await websocket.send_text(
            json.dumps(
                {
                    "type": "error",
                    "content": "Request rejected: specification appears malicious.",
                }
            )
        )
        await websocket.close()
        return

    async def emit(event: dict) -> None:
        await websocket.send_text(json.dumps(event))

    orchestrator = Orchestrator(spec=spec, repo=state.repo, emit=emit)
    try:
        await orchestrator.run()
    except Exception as exc:  # noqa: BLE001
        logger.exception("Orchestrator failed")
        await websocket.send_text(
            json.dumps(
                {
                    "type": "error",
                    "content": f"Unexpected error: {exc}",
                }
            )
        )
    finally:
        await websocket.close()


app.mount("/runs", StaticFiles(directory=RUNS_ROOT), name="runs")
app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="static")
