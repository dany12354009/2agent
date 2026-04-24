from __future__ import annotations

from pathlib import Path

from ..engine import AutoCutEngine
from ..exporters.capcut_exports import (
    export_effect_recommendations,
    export_keyframes_csv,
    export_timeline_json,
)
from ..models import EditStyle


def launch() -> None:
    try:
        from PySide6.QtWidgets import (
            QApplication,
            QComboBox,
            QFileDialog,
            QHBoxLayout,
            QLabel,
            QListWidget,
            QMainWindow,
            QPushButton,
            QTextEdit,
            QVBoxLayout,
            QWidget,
        )
    except Exception as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("PySide6 is required for desktop UI") from exc

    class MainWindow(QMainWindow):
        def __init__(self) -> None:
            super().__init__()
            self.setWindowTitle("AutoCut AI")
            self.resize(1100, 700)
            self.engine = AutoCutEngine()
            self.video_path: str | None = None
            self.plan = None

            root = QWidget()
            self.setCentralWidget(root)
            layout = QHBoxLayout(root)

            left = QVBoxLayout()
            self.preview = QLabel("Video preview placeholder")
            self.preview.setStyleSheet("background:#222;color:#eee;padding:20px;")
            self.timeline = QTextEdit()
            self.timeline.setReadOnly(True)
            self.timeline.setStyleSheet("background:#151515;color:#ddd;")
            left.addWidget(self.preview)
            left.addWidget(QLabel("Timeline / Edit plan"))
            left.addWidget(self.timeline)

            right = QVBoxLayout()
            self.subjects = QListWidget()
            self.style = QComboBox()
            self.style.addItems([s.value for s in EditStyle])

            import_btn = QPushButton("Import Video")
            auto_btn = QPushButton("Auto Edit")
            export_btn = QPushButton("Export to CapCut")

            import_btn.clicked.connect(self.import_video)
            auto_btn.clicked.connect(self.auto_edit)
            export_btn.clicked.connect(self.export)

            right.addWidget(QLabel("Detected subjects"))
            right.addWidget(self.subjects)
            right.addWidget(QLabel("Style"))
            right.addWidget(self.style)
            right.addWidget(import_btn)
            right.addWidget(auto_btn)
            right.addWidget(export_btn)

            layout.addLayout(left, 3)
            layout.addLayout(right, 1)
            root.setStyleSheet("background:#111;color:#f0f0f0;")

        def import_video(self) -> None:
            path, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.mov *.mkv)")
            if path:
                self.video_path = path
                self.preview.setText(f"Loaded: {Path(path).name}")

        def auto_edit(self) -> None:
            if not self.video_path:
                self.timeline.setPlainText("Please import a video first.")
                return

            style = EditStyle(self.style.currentText())
            self.plan = self.engine.auto_edit(self.video_path, style)
            self.subjects.clear()
            analysis = self.engine.analyze(self.video_path)
            for subject in analysis.detected_subjects:
                self.subjects.addItem(f"{subject.label} ({subject.confidence:.2f})")

            lines = [
                f"{a.timestamp:7.2f}s | {a.action:<16} | {a.effect:<10} | {a.reason}"
                for a in self.plan.actions
            ]
            self.timeline.setPlainText("\n".join(lines) if lines else "No suggested edits.")

        def export(self) -> None:
            if not self.plan:
                self.timeline.setPlainText("Run Auto Edit first.")
                return
            out_dir = Path(self.video_path).with_suffix("").as_posix() + "_autocut"
            out = Path(out_dir)
            out.mkdir(parents=True, exist_ok=True)
            export_timeline_json(self.plan, out / "timeline.json")
            export_keyframes_csv(self.plan, out / "keyframes.csv")
            export_effect_recommendations(self.plan, out / "effects.json")
            self.timeline.append(f"\nExported files to: {out}")

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
