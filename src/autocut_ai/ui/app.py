from __future__ import annotations

from pathlib import Path

from ..app.application import create_service
from ..decision.styles import STYLE_PROFILES


def launch() -> None:
    try:
        from PySide6.QtCore import Qt
        from PySide6.QtWidgets import (
            QApplication,
            QCheckBox,
            QComboBox,
            QFileDialog,
            QHBoxLayout,
            QLabel,
            QListWidget,
            QMainWindow,
            QPushButton,
            QProgressBar,
            QSlider,
            QStackedWidget,
            QTextEdit,
            QVBoxLayout,
            QWidget,
        )
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("PySide6 is required for desktop UI") from exc

    class MainWindow(QMainWindow):
        def __init__(self) -> None:
            super().__init__()
            self.setWindowTitle("AutoCut AI")
            self.resize(1280, 760)
            self.service = create_service("free")
            self.video_path: str | None = None
            self.result = None

            self.stack = QStackedWidget()
            self.setCentralWidget(self.stack)
            self.stack.addWidget(self._build_import_screen())
            self.stack.addWidget(self._build_progress_screen())
            self.stack.addWidget(self._build_dashboard())

            self.setStyleSheet(
                """
                QWidget { background:#111; color:#f5f5f5; }
                QPushButton { background:#292929; padding:8px; border-radius:6px; }
                QPushButton:hover { background:#3a3a3a; }
                QTextEdit, QListWidget { background:#171717; border:1px solid #2a2a2a; }
                """
            )

        def _build_import_screen(self) -> QWidget:
            page = QWidget()
            layout = QVBoxLayout(page)
            title = QLabel("Import Screen")
            title.setStyleSheet("font-size:24px;font-weight:700;")
            self.import_status = QLabel("No video selected")
            select_btn = QPushButton("Select Video")
            continue_btn = QPushButton("Start Analysis")
            select_btn.clicked.connect(self.select_video)
            continue_btn.clicked.connect(self.start_analysis)
            layout.addWidget(title)
            layout.addWidget(self.import_status)
            layout.addWidget(select_btn)
            layout.addWidget(continue_btn)
            layout.addStretch()
            return page

        def _build_progress_screen(self) -> QWidget:
            page = QWidget()
            layout = QVBoxLayout(page)
            title = QLabel("Analysis Progress")
            title.setStyleSheet("font-size:24px;font-weight:700;")
            self.progress_label = QLabel("Waiting to start...")
            self.progress = QProgressBar()
            self.progress.setRange(0, 100)
            back_btn = QPushButton("Back")
            back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
            layout.addWidget(title)
            layout.addWidget(self.progress_label)
            layout.addWidget(self.progress)
            layout.addWidget(back_btn)
            layout.addStretch()
            return page

        def _build_dashboard(self) -> QWidget:
            page = QWidget()
            layout = QHBoxLayout(page)

            left = QVBoxLayout()
            self.preview = QLabel("Video Preview Player (prototype)")
            self.preview.setMinimumHeight(220)
            self.preview.setStyleSheet("background:#1d1d1d;padding:16px;")
            self.timeline = QTextEdit()
            self.timeline.setReadOnly(True)
            left.addWidget(self.preview)
            left.addWidget(QLabel("Timeline + Layers"))
            left.addWidget(self.timeline)

            right = QVBoxLayout()
            self.subjects = QListWidget()
            self.style_box = QComboBox()
            self.style_box.addItems(sorted(STYLE_PROFILES.keys()))
            self.intensity = QSlider(Qt.Horizontal)
            self.intensity.setRange(10, 100)
            self.intensity.setValue(70)
            self.overlay_tracking = QCheckBox("Show tracking boxes")
            self.overlay_attention = QCheckBox("Show attention heatmap")
            run_btn = QPushButton("Re-run Auto Edit")
            export_btn = QPushButton("Export to CapCut")
            run_btn.clicked.connect(self.run_edit)
            export_btn.clicked.connect(self.export)

            right.addWidget(QLabel("Detected Subjects"))
            right.addWidget(self.subjects)
            right.addWidget(QLabel("Style Profile"))
            right.addWidget(self.style_box)
            right.addWidget(QLabel("Edit Intensity"))
            right.addWidget(self.intensity)
            right.addWidget(self.overlay_tracking)
            right.addWidget(self.overlay_attention)
            right.addWidget(run_btn)
            right.addWidget(export_btn)
            right.addStretch()

            layout.addLayout(left, 3)
            layout.addLayout(right, 2)
            return page

        def select_video(self) -> None:
            path, _ = QFileDialog.getOpenFileName(self, "Open video", "", "Video Files (*.mp4 *.mov *.mkv)")
            if path:
                self.video_path = path
                self.import_status.setText(f"Selected: {Path(path).name}")

        def start_analysis(self) -> None:
            if not self.video_path:
                self.import_status.setText("Select a video first")
                return
            self.stack.setCurrentIndex(1)
            self.progress_label.setText("Running multi-module analysis...")
            self.progress.setValue(35)
            self.run_edit()
            self.progress.setValue(100)
            self.progress_label.setText("Analysis complete")
            self.stack.setCurrentIndex(2)

        def run_edit(self) -> None:
            if not self.video_path:
                return
            style = self.style_box.currentText()
            self.service.config.product.edit_intensity = self.intensity.value() / 100.0
            self.result = self.service.process_clip(self.video_path, style)
            self.preview.setText(
                f"Loaded: {Path(self.video_path).name}\n"
                f"Overlays tracking={self.overlay_tracking.isChecked()} attention={self.overlay_attention.isChecked()}"
            )
            self.subjects.clear()
            for subject in self.result.timeline.actions[:20]:
                self.subjects.addItem(f"{subject.tracking_target} :: {subject.effect}")
            lines = [
                f"{a.timestamp:6.2f}s | {a.effect:<12} | intensity={a.intensity:.2f} | {a.reason}"
                for a in self.result.plan.actions
            ]
            warnings = "\n".join(f"⚠ {w}" for w in self.result.warnings)
            self.timeline.setPlainText(("\n".join(lines) or "No actions") + ("\n\n" + warnings if warnings else ""))

        def export(self) -> None:
            if not self.result or not self.video_path:
                return
            out_dir = Path(self.video_path).with_suffix("").as_posix() + "_autocut"
            paths = self.service.export_all(self.result, out_dir)
            self.timeline.append(f"\n\nExport complete:\n{paths}")

    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()
