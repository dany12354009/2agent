"""Workspace management utilities for DuoForge."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence
from zipfile import ZIP_DEFLATED, ZipFile


@dataclass
class RepoManager:
    """Encapsulates the per-session workspace on disk."""

    run_root: Path

    def __post_init__(self) -> None:
        self.run_root.mkdir(parents=True, exist_ok=True)
        self.workspace = self.run_root / "workspace"
        self.workspace.mkdir(parents=True, exist_ok=True)

    def _ensure_within_workspace(self, path: Path) -> Path:
        resolved = (self.workspace / path).resolve()
        if not str(resolved).startswith(str(self.workspace.resolve())):
            raise ValueError(f"Path escapes workspace: {path}")
        resolved.parent.mkdir(parents=True, exist_ok=True)
        return resolved

    def snapshot(self, max_chars: int = 16_000) -> List[dict]:
        """Return a truncated list of files and their contents."""

        files: List[dict] = []
        consumed = 0
        for file_path in sorted(self.workspace.rglob("*")):
            if file_path.is_dir():
                continue
            rel_path = file_path.relative_to(self.workspace).as_posix()
            try:
                content = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                content = "<binary>"
            entry = {"path": rel_path, "content": content}
            entry_str = json.dumps(entry, ensure_ascii=False)
            consumed += len(entry_str)
            if consumed > max_chars:
                break
            files.append(entry)
        return files

    def apply_changes(self, changes: Sequence[dict]) -> None:
        for change in changes:
            ctype = change.get("type")
            path_str = change.get("path")
            if ctype not in {"new", "patch"}:
                raise ValueError(f"Unsupported change type: {ctype}")
            if not path_str:
                raise ValueError("Change missing path")
            target_path = self._ensure_within_workspace(Path(path_str))

            if ctype == "new":
                content = change.get("content", "")
                target_path.write_text(content, encoding="utf-8")
            elif ctype == "patch":
                patch_text = change.get("patch", "")
                if "@@" not in patch_text:
                    # Treat as full replacement
                    target_path.write_text(patch_text, encoding="utf-8")
                    continue
                original = ""
                if target_path.exists():
                    original = target_path.read_text(encoding="utf-8")
                try:
                    updated = apply_unified_diff(original, patch_text)
                except ValueError:
                    # Fallback to full replacement semantics
                    updated = patch_text
                target_path.write_text(updated, encoding="utf-8")

    def ensure_readme(self, spec: str, plan_json: dict) -> None:
        readme_path = self._ensure_within_workspace(Path("README.md"))
        plan_str = json.dumps(plan_json, indent=2, ensure_ascii=False)
        content = (
            "# DuoForge build\n\n"
            "## User specification\n\n"
            f"{spec}\n\n"
            "## Implementation plan\n\n"
            f"```json\n{plan_str}\n```\n"
        )
        readme_path.write_text(content, encoding="utf-8")

    def zip_out(self) -> str:
        out_path = self.run_root / "out.zip"
        with ZipFile(out_path, "w", ZIP_DEFLATED) as zip_file:
            for file_path in self.workspace.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(self.workspace)
                    zip_file.write(file_path, arcname.as_posix())
        return f"/runs/{self.run_root.name}/out.zip"


_HEADER_RE = re.compile(r"@@ -(?P<start_old>\d+)(?:,(?P<count_old>\d+))? \+(?P<start_new>\d+)(?:,(?P<count_new>\d+))? @@")


def apply_unified_diff(original: str, diff_text: str) -> str:
    """Apply a unified diff string to the original text."""

    orig_lines = original.splitlines(keepends=True)
    out_lines: List[str] = []
    index = 0
    lines = diff_text.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i]
        if line.startswith("---") or line.startswith("+++"):
            i += 1
            continue
        if line.startswith("@@"):
            match = _HEADER_RE.match(line)
            if not match:
                raise ValueError("Invalid hunk header")
            start_old = int(match.group("start_old")) - 1
            while index < start_old and index < len(orig_lines):
                out_lines.append(orig_lines[index])
                index += 1
            i += 1
            while i < len(lines) and not lines[i].startswith("@@"):
                hunk_line = lines[i]
                if hunk_line.startswith(" "):
                    if index >= len(orig_lines):
                        raise ValueError("Context line out of range")
                    out_lines.append(orig_lines[index])
                    index += 1
                elif hunk_line.startswith("-"):
                    if index >= len(orig_lines):
                        raise ValueError("Deletion line out of range")
                    index += 1
                elif hunk_line.startswith("+"):
                    text = hunk_line[1:]
                    if not text.endswith("\n"):
                        text += "\n"
                    out_lines.append(text)
                elif hunk_line == "\\ No newline at end of file":
                    # Ignore marker; the previous line already omits newline
                    pass
                else:
                    raise ValueError("Unknown diff line type")
                i += 1
        else:
            i += 1

    while index < len(orig_lines):
        out_lines.append(orig_lines[index])
        index += 1

    return "".join(out_lines)
