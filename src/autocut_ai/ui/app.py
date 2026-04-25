from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Qt, QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QSlider,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..app.application import create_service
from ..decision.styles import STYLE_PROFILES
from ..integrations.capcut_automation import CapCutCompanion


class AnalysisWorker(QObject):
    finished = Signal(object)
    failed = Signal(str)

    def __init__(self, service, video_path: str, style: str, intensity: float) -> None:
        super().__init__()
        self.service = service
        self.video_path = video_path
        self.style = style
        self.intensity = intensity

    def run(self) -> None:
        try:
            self.service.config.product.edit_intensity = self.intensity
            result = self.service.process_clip(self.video_path, self.style)
            self.finished.emit(result)
        except Exception as exc:  # pragma: no cover
            self.failed.emit(str(exc))


def launch() -> None:
    class MainWindow(QMainWindow):
        def __init__(self) -> None:
            super().__init__()
            self.setWindowTitle("AutoCut AI Studio")
            self.resize(1400, 820)

            self.service = create_service("free")
            self.video_path: str | None = None
            self.result = None

            self.stack = QStackedWidget()
            self.setCentralWidget(self.stack)
            self.stack.addWidget(self._build_import_page())
            self.stack.addWidget(self._build_progress_page())
            self.stack.addWidget(self._build_editor_page())

            self.setStyleSheet(
                """
                QWidget { background:#111; color:#f5f5f5; font-size:13px; }
                QGroupBox { border:1px solid #2a2a2a; margin-top:8px; padding:10px; }
                QPushButton { background:#2b2b2b; border:1px solid #404040; border-radius:6px; padding:8px; }
                QPushButton:hover { background:#3b3b3b; }
                QTextEdit, QTableWidget, QComboBox { background:#181818; border:1px solid #2f2f2f; }
                """
            )

        def _build_import_page(self) -> QWidget:
            page = QWidget()
            layout = QVBoxLayout(page)
            title = QLabel("Import Project")
            title.setStyleSheet("font-size:26px;font-weight:700;")
            subtitle = QLabel("Choose a clip and editing style to begin AI analysis.")
            self.import_status = QLabel("No video selected")
            self.import_style = QComboBox()
            self.import_style.addItems(sorted(STYLE_PROFILES.keys()))
            self.import_intensity = QSlider(Qt.Horizontal)
            self.import_intensity.setRange(10, 100)
            self.import_intensity.setValue(70)

            row = QHBoxLayout()
            btn_pick = QPushButton("Select Video")
            btn_start = QPushButton("Analyze")
            btn_pick.clicked.connect(self._select_video)
            btn_start.clicked.connect(self._start_analysis)
            row.addWidget(btn_pick)
            row.addWidget(btn_start)

            layout.addWidget(title)
            layout.addWidget(subtitle)
            layout.addWidget(self.import_status)
            layout.addWidget(QLabel("Style"))
            layout.addWidget(self.import_style)
            layout.addWidget(QLabel("Edit intensity"))
            layout.addWidget(self.import_intensity)
            layout.addLayout(row)
            layout.addStretch()
            return page

        def _build_progress_page(self) -> QWidget:
            page = QWidget()
            layout = QVBoxLayout(page)
            title = QLabel("Analysis in progress")
            title.setStyleSheet("font-size:24px;font-weight:700;")
            self.progress = QProgressBar()
            self.progress.setRange(0, 0)
            self.progress_log = QTextEdit()
            self.progress_log.setReadOnly(True)
            btn_cancel = QPushButton("Back")
            btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))
            layout.addWidget(title)
            layout.addWidget(self.progress)
            layout.addWidget(self.progress_log)
            layout.addWidget(btn_cancel)
            return page

        def _build_editor_page(self) -> QWidget:
            page = QWidget()
            layout = QGridLayout(page)

            preview_box = QGroupBox("Preview + Overlay")
            preview_layout = QVBoxLayout(preview_box)
            self.preview = QLabel("No preview loaded")
            self.preview.setMinimumHeight(220)
            self.preview.setStyleSheet("background:#1d1d1d;padding:12px;")
            self.overlay_tracking = QCheckBox("Tracking boxes")
            self.overlay_attention = QCheckBox("Attention heatmap")
            preview_layout.addWidget(self.preview)
            preview_layout.addWidget(self.overlay_tracking)
            preview_layout.addWidget(self.overlay_attention)

            actions_box = QGroupBox("Timeline Actions")
            actions_layout = QVBoxLayout(actions_box)
            self.actions_table = QTableWidget(0, 5)
            self.actions_table.setHorizontalHeaderLabels(["Time", "Effect", "Target", "Intensity", "Reason"])
            self.actions_table.horizontalHeader().setStretchLastSection(True)
            actions_layout.addWidget(self.actions_table)

            control_box = QGroupBox("Controls")
            control_layout = QVBoxLayout(control_box)
            self.editor_style = QComboBox()
            self.editor_style.addItems(sorted(STYLE_PROFILES.keys()))
            self.editor_intensity = QSlider(Qt.Horizontal)
            self.editor_intensity.setRange(10, 100)
            self.editor_intensity.setValue(70)
            self.manual_tools = QTextEdit()
            self.manual_tools.setReadOnly(True)
            self.manual_tools.setPlainText(
                "Manual Override Tools\n"
                "- Drag tracking boxes (coming soon)\n"
                "- Adjust zoom anchors (coming soon)\n"
                "- Re-target main subject (coming soon)"
            )
            btn_rerun = QPushButton("Re-run Analysis")
            btn_export = QPushButton("Export to CapCut")
            btn_companion = QPushButton("Show Companion Steps")
            btn_rerun.clicked.connect(self._rerun_from_editor)
            btn_export.clicked.connect(self._export)
            btn_companion.clicked.connect(self._show_companion)

            control_layout.addWidget(QLabel("Style"))
            control_layout.addWidget(self.editor_style)
            control_layout.addWidget(QLabel("Intensity"))
            control_layout.addWidget(self.editor_intensity)
            control_layout.addWidget(self.manual_tools)
            control_layout.addWidget(btn_rerun)
            control_layout.addWidget(btn_export)
            control_layout.addWidget(btn_companion)

            summary_box = QGroupBox("Analysis Summary")
            summary_layout = QVBoxLayout(summary_box)
            self.summary = QTextEdit()
            self.summary.setReadOnly(True)
            summary_layout.addWidget(self.summary)

            layout.addWidget(preview_box, 0, 0)
            layout.addWidget(control_box, 0, 1)
            layout.addWidget(actions_box, 1, 0, 1, 2)
            layout.addWidget(summary_box, 0, 2, 2, 1)
            layout.setColumnStretch(0, 3)
            layout.setColumnStretch(1, 2)
            layout.setColumnStretch(2, 2)
            return page

        def _select_video(self) -> None:
            path, _ = QFileDialog.getOpenFileName(self, "Select video", "", "Video Files (*.mp4 *.mov *.mkv)")
            if path:
                self.video_path = path
                self.import_status.setText(f"Selected: {Path(path).name}")

        def _start_analysis(self) -> None:
            if not self.video_path:
                QMessageBox.warning(self, "Missing video", "Please select a video first.")
                return
            self.stack.setCurrentIndex(1)
            self.progress_log.setPlainText("Queued: frame extraction\nQueued: analysis pipeline\nQueued: decision engine")
            self._run_worker(self.import_style.currentText(), self.import_intensity.value() / 100)

        def _rerun_from_editor(self) -> None:
            if not self.video_path:
                return
            self.stack.setCurrentIndex(1)
            self.progress_log.setPlainText("Re-running with updated style/intensity...")
            self._run_worker(self.editor_style.currentText(), self.editor_intensity.value() / 100)

        def _run_worker(self, style: str, intensity: float) -> None:
            self.thread = QThread(self)
            self.worker = AnalysisWorker(self.service, self.video_path, style, intensity)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self._on_analysis_success)
            self.worker.failed.connect(self._on_analysis_failed)
            self.worker.finished.connect(self.thread.quit)
            self.worker.failed.connect(self.thread.quit)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()

        def _on_analysis_success(self, result) -> None:
            self.result = result
            self.stack.setCurrentIndex(2)
            self.preview.setText(
                f"Clip: {Path(self.video_path).name}\n"
                f"Overlay tracking={self.overlay_tracking.isChecked()} attention={self.overlay_attention.isChecked()}"
            )
            self.actions_table.setRowCount(len(result.plan.actions))
            for row, action in enumerate(result.plan.actions):
                self.actions_table.setItem(row, 0, QTableWidgetItem(f"{action.timestamp:.2f}s"))
                self.actions_table.setItem(row, 1, QTableWidgetItem(action.effect))
                self.actions_table.setItem(row, 2, QTableWidgetItem(action.tracking_target))
                self.actions_table.setItem(row, 3, QTableWidgetItem(f"{action.intensity:.2f}"))
                self.actions_table.setItem(row, 4, QTableWidgetItem(action.reason))

            warnings = "\n".join(f"- {w}" for w in result.warnings) or "- none"
            self.summary.setPlainText(
                f"Actions: {len(result.plan.actions)}\n"
                f"Style: {result.plan.style}\n"
                f"Warnings:\n{warnings}"
            )

        def _on_analysis_failed(self, error: str) -> None:
            QMessageBox.critical(self, "Analysis failed", error)
            self.stack.setCurrentIndex(0)

        def _export(self) -> None:
            if not self.result or not self.video_path:
                return
            out_dir = Path(self.video_path).with_suffix("").as_posix() + "_autocut"
            paths = self.service.export_all(self.result, out_dir)
            QMessageBox.information(self, "Export complete", "\n".join(f"{k}: {v}" for k, v in paths.items()))

        def _show_companion(self) -> None:
            if not self.result or not self.video_path:
                QMessageBox.information(self, "Companion", "Export first to generate companion guidance.")
                return
            out_dir = Path(self.video_path).with_suffix("").as_posix() + "_autocut"
            paths = self.service.export_all(self.result, out_dir)
            steps = CapCutCompanion().build_steps(paths)
            QMessageBox.information(self, "CapCut Companion", "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps)))

    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()
