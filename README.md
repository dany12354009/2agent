# AutoCut AI (Local Prototype)

AutoCut AI is a desktop-first local video editing assistant that analyzes raw clips and generates a CapCut-ready edit plan.

## What this prototype does

- Imports a video clip.
- Runs local-first analysis modules for:
  - Scene change detection (OpenCV histogram-diff).
  - Motion intensity analysis (OpenCV frame differencing).
  - Beat detection (Librosa, optional).
  - Subject detection/tracking (YOLO optional, with lightweight fallback).
- Detects a **main subject** and builds edit actions:
  - zoom emphasis on motion
  - beat cuts
  - scene flash transitions
- Supports editing styles:
  - gaming short
  - cinematic
  - meme
  - fast tiktok
  - dramatic slowmo
  - clean shorts
- Exports for CapCut workflows:
  - `timeline.json` (edit decision list)
  - `keyframes.csv` (crop/zoom-compatible keyframes)
  - `effects.json` (recommended effect timestamps)

## Architecture

```text
Video -> Load/Frame Sample
      -> Analyze (scene/motion/audio/subject)
      -> Main Subject Selection
      -> Style-aware Edit Planner
      -> CapCut Exporters (JSON/CSV)
      -> Optional UI Automation module
```

Key modules:
- `autocut_ai/engine.py`: orchestration.
- `autocut_ai/analyzers/*`: pluggable local AI / CV analyzers.
- `autocut_ai/planner.py`: style-aware plan generation.
- `autocut_ai/exporters/*`: CapCut bridge outputs.
- `autocut_ai/ui/app.py`: PySide6 dark desktop UI.
- `autocut_ai/integrations/capcut_automation.py`: optional automation layer.

## Install

Minimal (for structure/tests):

```bash
pip install -e .
```

Full local AI stack (optional):

```bash
pip install -e '.[full]'
```

Dev tools:

```bash
pip install -e '.[dev]'
```

## CLI usage

```bash
python -m autocut_ai.cli /path/to/video.mp4 --style gaming_short --out out_dir
```

## Desktop UI

```bash
python -c "from autocut_ai.ui.app import launch; launch()"
```

## Extending models

This repo intentionally keeps analyzers modular:
- Swap YOLO models in `SubjectAnalyzer._run_yolo`.
- Add MediaPipe face/body weighting in `SubjectAnalyzer`.
- Add Whisper subtitle extraction module and pass captions to `export_srt`.
- Add new styles by extending `EditStyle` + `STYLE_EFFECT_PRESETS`.

## Safety note on CapCut automation

UI automation is disabled by default and should be user-confirmed due to desktop-control risk. Use exported artifacts for manual import as the default workflow.
