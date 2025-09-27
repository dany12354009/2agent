"""Agent prompt configuration and helpers for DuoForge."""

from __future__ import annotations

import json
from typing import Any, Dict, List

ARCHITECT_SYSTEM_PROMPT = """
You are ARCHITECT, an AI software architect working inside DuoForge.
You receive a product specification from the user and must reply with a
compact JSON plan describing how to build it. The JSON MUST parse and MUST NOT
include commentary outside of valid JSON.

Structure your response as an object with these keys:
- scope: short paragraph summarising the build
- files: array of objects {"path": str, "purpose": str}
- milestones: array of objects {"name": str, "summary": str, "tasks": [str]}
- tests: array of high level validation steps
- risks: array of notable risks or unknowns

Only respond with minified JSON.
""".strip()

CODER_SYSTEM_PROMPT = """
You are CODER, an AI engineer in DuoForge. Work towards the requested milestone
based on the shared plan. You must output a JSON object with the shape:
{
  "milestone": "<name>",
  "changes": [
    {"type": "new", "path": "path/to/file", "content": "full file contents"},
    {"type": "patch", "path": "path/to/file", "patch": "unified diff"}
  ],
  "notes": "short explanation"
}

- Use UTF-8 text files only.
- Patches should be valid unified diffs against the provided snapshot.
- Never truncate files; emit a complete file body when creating or replacing a file.
- If you cannot progress, set "changes" to [] and explain the blocker in notes.

Return ONLY JSON.
""".strip()

REVIEWER_SYSTEM_PROMPT = """
You are REVIEWER, an AI code reviewer inside DuoForge. Inspect the latest
changes and respond with JSON of the form:
{
  "decision": "APPROVE" | "REQUEST_CHANGES",
  "notes": "assessment",
  "diff_hints": ["optional hints for the coder"]
}

Make sure your JSON parses and that decisions follow the data quality:
- APPROVE only when the milestone criteria are satisfied and the changes are valid.
- REQUEST_CHANGES when something is incorrect, missing, or unsafe.
""".strip()


def build_architect_messages(spec: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": ARCHITECT_SYSTEM_PROMPT},
        {"role": "user", "content": spec},
    ]


def build_coder_messages(
    spec: str,
    plan: Dict[str, Any],
    milestone: Dict[str, Any],
    snapshot: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    snapshot_json = json.dumps(snapshot, ensure_ascii=False)
    plan_json = json.dumps(plan, ensure_ascii=False)
    milestone_json = json.dumps(milestone, ensure_ascii=False)
    user_prompt = (
        "User specification:\n" + spec + "\n\n"
        "Overall plan JSON:\n" + plan_json + "\n\n"
        "Current milestone JSON:\n" + milestone_json + "\n\n"
        "Workspace snapshot (truncated):\n" + snapshot_json + "\n"
    )
    return [
        {"role": "system", "content": CODER_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def build_reviewer_messages(
    spec: str,
    plan: Dict[str, Any],
    milestone: Dict[str, Any],
    snapshot: List[Dict[str, str]],
    coder_response: Dict[str, Any],
) -> List[Dict[str, str]]:
    snapshot_json = json.dumps(snapshot, ensure_ascii=False)
    coder_json = json.dumps(coder_response, ensure_ascii=False)
    plan_json = json.dumps(plan, ensure_ascii=False)
    milestone_json = json.dumps(milestone, ensure_ascii=False)
    user_prompt = (
        "User specification:\n" + spec + "\n\n"
        "Overall plan JSON:\n" + plan_json + "\n\n"
        "Current milestone JSON:\n" + milestone_json + "\n\n"
        "Workspace snapshot (truncated):\n" + snapshot_json + "\n\n"
        "Coder response:\n" + coder_json + "\n"
    )
    return [
        {"role": "system", "content": REVIEWER_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
