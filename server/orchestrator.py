"""Agent orchestration loop for DuoForge."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict

from . import agents, llm
from .repo import RepoManager

logger = logging.getLogger(__name__)

EventEmitter = Callable[[Dict[str, Any]], Awaitable[None]]


@dataclass
class Orchestrator:
    spec: str
    repo: RepoManager
    emit: EventEmitter
    max_cycles: int = 3

    async def run(self) -> None:
        plan_content = await self._call_architect()
        try:
            plan_json = json.loads(plan_content)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Architect returned invalid JSON") from exc

        await self.emit({"type": "plan", "from_agent": "Architect", "content": plan_content})
        self.repo.ensure_readme(self.spec, plan_json)

        milestones = plan_json.get("milestones") or []
        if not isinstance(milestones, list) or not milestones:
            milestones = [{"name": "Build", "summary": "Complete build", "tasks": []}]

        for index, milestone in enumerate(milestones, start=1):
            if "name" not in milestone:
                milestone["name"] = f"Milestone {index}"
            await self._run_milestone(plan_json, milestone)

        zip_url = self.repo.zip_out()
        await self.emit({"type": "zip_ready", "url": zip_url})

    async def _call_architect(self) -> str:
        messages = agents.build_architect_messages(self.spec)
        return await llm.chat(messages)

    async def _run_milestone(self, plan_json: Dict[str, Any], milestone: Dict[str, Any]) -> None:
        cycles = 0
        while cycles < self.max_cycles:
            snapshot = self.repo.snapshot()
            coder_messages = agents.build_coder_messages(self.spec, plan_json, milestone, snapshot)
            coder_raw = await llm.chat(coder_messages)
            await self.emit({"type": "diff", "from_agent": "Coder", "content": coder_raw})

            try:
                coder_json = json.loads(coder_raw)
            except json.JSONDecodeError:
                reviewer_notes = {
                    "decision": "REQUEST_CHANGES",
                    "notes": "Coder response was not valid JSON.",
                    "diff_hints": ["Ensure the response is strictly valid JSON."],
                }
                await self.emit({"type": "review", "from_agent": "Reviewer", "content": json.dumps(reviewer_notes)})
                cycles += 1
                continue

            changes = coder_json.get("changes", [])
            try:
                self.repo.apply_changes(changes)
            except Exception as exc:  # noqa: BLE001
                reviewer_notes = {
                    "decision": "REQUEST_CHANGES",
                    "notes": f"Failed to apply changes: {exc}",
                    "diff_hints": ["Double-check the diff formatting."],
                }
                await self.emit({"type": "review", "from_agent": "Reviewer", "content": json.dumps(reviewer_notes)})
                cycles += 1
                continue

            snapshot_after = self.repo.snapshot()
            reviewer_messages = agents.build_reviewer_messages(
                self.spec,
                plan_json,
                milestone,
                snapshot_after,
                coder_json,
            )
            review_raw = await llm.chat(reviewer_messages)
            await self.emit({"type": "review", "from_agent": "Reviewer", "content": review_raw})

            try:
                review_json = json.loads(review_raw)
            except json.JSONDecodeError:
                cycles += 1
                continue

            decision = review_json.get("decision", "REQUEST_CHANGES")
            if decision == "APPROVE":
                return
            cycles += 1

        logger.warning("Milestone '%s' exceeded max cycles", milestone.get("name"))
