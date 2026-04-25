from __future__ import annotations

from pathlib import Path


def export_srt(captions: list[tuple[float, float, str]], output_path: str) -> Path:
    """Export subtitle tuples as SRT. Captions come from local Whisper or manual input."""

    def fmt(ts: float) -> str:
        h = int(ts // 3600)
        m = int((ts % 3600) // 60)
        s = int(ts % 60)
        ms = int((ts - int(ts)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    lines: list[str] = []
    for i, (start, end, text) in enumerate(captions, start=1):
        lines.extend([str(i), f"{fmt(start)} --> {fmt(end)}", text, ""])

    path = Path(output_path)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
