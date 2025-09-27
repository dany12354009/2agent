from __future__ import annotations

import json
from pathlib import Path

from server.repo import RepoManager, apply_unified_diff


def test_apply_unified_diff_addition(tmp_path: Path) -> None:
    original = "line1\nline2\n"
    diff = """--- a/file.txt\n+++ b/file.txt\n@@ -1,2 +1,3 @@\n line1\n+line1.5\n line2\n"""
    result = apply_unified_diff(original, diff)
    assert result == "line1\nline1.5\nline2\n"


def test_repo_manager_apply_and_snapshot(tmp_path: Path) -> None:
    manager = RepoManager(tmp_path)
    manager.apply_changes(
        [
            {"type": "new", "path": "foo.txt", "content": "alpha\n"},
            {"type": "new", "path": "bar/baz.txt", "content": "beta"},
        ]
    )

    snapshot = manager.snapshot()
    paths = {entry["path"] for entry in snapshot}
    assert paths == {"foo.txt", "bar/baz.txt"}

    manager.apply_changes(
        [
            {
                "type": "patch",
                "path": "foo.txt",
                "patch": "--- a/foo.txt\n+++ b/foo.txt\n@@ -1,1 +1,2 @@\n alpha\n+gamma\n",
            }
        ]
    )
    assert (manager.workspace / "foo.txt").read_text(encoding="utf-8") == "alpha\ngamma\n"


def test_ensure_readme_and_zip(tmp_path: Path) -> None:
    manager = RepoManager(tmp_path)
    plan = {"milestones": [], "scope": "test"}
    manager.ensure_readme("Spec", plan)
    readme_content = (manager.workspace / "README.md").read_text(encoding="utf-8")
    assert "Spec" in readme_content
    assert json.dumps(plan, indent=2) in readme_content

    zip_url = manager.zip_out()
    assert zip_url.endswith("/out.zip")
    assert (manager.run_root / "out.zip").exists()
