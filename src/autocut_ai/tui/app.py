from __future__ import annotations

import curses
from pathlib import Path

from ..app.application import create_service
from ..decision.styles import STYLE_PROFILES
from ..integrations.capcut_automation import CapCutCompanion
from ..services.product_service import ProcessingResult
from .views import TUIViewModel, render_header, render_result_lines


def launch_tui() -> None:
    curses.wrapper(_run)


def _prompt(stdscr: curses.window, message: str) -> str:
    curses.echo()
    height, _ = stdscr.getmaxyx()
    stdscr.addstr(height - 1, 0, " " * 120)
    stdscr.addstr(height - 1, 0, message)
    stdscr.refresh()
    value = stdscr.getstr(height - 1, len(message), 100).decode("utf-8").strip()
    curses.noecho()
    return value


def _run(stdscr: curses.window) -> None:
    service = create_service("free")
    companion = CapCutCompanion()
    model = TUIViewModel()
    styles = sorted(STYLE_PROFILES.keys())
    style_index = styles.index(model.style)
    result: ProcessingResult | None = None
    exports: dict[str, str] = {}

    curses.curs_set(0)
    stdscr.nodelay(False)

    while True:
        stdscr.erase()
        y = 0
        for line in render_header(model):
            stdscr.addstr(y, 0, line[:150])
            y += 1
        y += 1

        stdscr.addstr(y, 0, "Controls: i=input path  s=style  +/-=intensity  o=output dir  r=run  e=export  c=companion  q=quit")
        y += 2

        for line in render_result_lines(result):
            if y >= curses.LINES - 2:
                break
            stdscr.addstr(y, 0, line[:150])
            y += 1

        if exports:
            if y < curses.LINES - 2:
                stdscr.addstr(y, 0, "")
                y += 1
            for key, value in exports.items():
                if y >= curses.LINES - 2:
                    break
                stdscr.addstr(y, 0, f"{key}: {value}"[:150])
                y += 1

        stdscr.refresh()
        key = stdscr.getch()

        if key in (ord("q"), 27):
            return
        if key == ord("i"):
            value = _prompt(stdscr, "Video path: ")
            if value:
                model.video_path = value
                model.status = f"Video set: {Path(value).name}"
        elif key == ord("o"):
            value = _prompt(stdscr, "Output directory: ")
            if value:
                model.output_dir = value
                model.status = f"Output dir set: {value}"
        elif key == ord("s"):
            style_index = (style_index + 1) % len(styles)
            model.style = styles[style_index]
            model.status = f"Style changed to {model.style}"
        elif key == ord("+"):
            model.intensity = min(1.0, model.intensity + 0.05)
            model.status = "Intensity increased"
        elif key == ord("-"):
            model.intensity = max(0.1, model.intensity - 0.05)
            model.status = "Intensity decreased"
        elif key == ord("r"):
            if not model.video_path:
                model.status = "Set video path first"
                continue
            try:
                service.config.product.edit_intensity = model.intensity
                result = service.process_clip(model.video_path, model.style)
                model.status = f"Analysis complete ({len(result.plan.actions)} actions)"
            except Exception as exc:
                model.status = f"Run failed: {exc}"
        elif key == ord("e"):
            if result is None:
                model.status = "Run analysis first"
                continue
            try:
                out = Path(model.output_dir) / Path(model.video_path).stem
                exports = service.export_all(result, str(out))
                model.status = f"Exported to {out}"
            except Exception as exc:
                model.status = f"Export failed: {exc}"
        elif key == ord("c"):
            if not exports:
                model.status = "Export first to open companion guide"
                continue
            steps = companion.build_steps(exports)
            model.status = " | ".join(steps[:2])
