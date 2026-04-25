# AutoCut AI — Production-Oriented Local Desktop Editor

AutoCut AI is a local-first AI editing assistant for short-form video (TikTok, Shorts, Reels). This codebase is structured as a production-ready desktop product with modular analysis, decision logic, timeline generation, and CapCut integration modes.

## Product Architecture

### 1) Video Processing Engine
- Multi-resolution frame extraction with threaded resizing.
- Video metadata handling and cache metadata persistence.
- Sampling controls for light/full analysis modes.

### 2) AI Analysis Engine
- Independent modules feeding a central graph:
  - Detection (`YOLO` when available, fallback otherwise)
  - Tracking (hook point for SORT/DeepSORT)
  - Face/body confidence boosting (`MediaPipe` optional)
  - Scene cuts
  - Motion spikes
  - Audio beats (`librosa` optional)
  - Speech (`whisper` optional)

### 3) Scene Intelligence Graph (Core)
- Central temporal graph storing:
  - subjects and track states
  - events (beats, action spikes, transitions, speech)
  - low-confidence warnings
- All edit decisions are derived from this graph.

### 4) Edit Decision Engine
- Layered editing intelligence:
  - **Attention model** (event confidence + center bias + style intensity)
  - **Rhythm engine** (beat-aligned cuts)
  - **Cinematic rules** (shake anti-spam, continuity transitions)
  - **Style profiles** (`gaming_short`, `cinematic`, `viral_shorts`, `clean_shorts`)

### 5) Timeline Generator
- Generates timeline tracks/layers:
  - video base track
  - effects track
  - captions track

## Desktop UX

PySide6 desktop app includes:
- Import Screen
- Analysis Progress Screen (background worker thread)
- Editor Dashboard with:
  - preview/overlay panel
  - timeline action table
  - style selector + intensity slider
  - manual override panel placeholders
  - analysis summary panel
  - export and companion guide buttons

Terminal UI (`curses`) includes:
- keyboard-driven workflow for path/style/intensity
- run analysis + export without GUI
- action/warning preview in terminal

## CapCut Integration Modes

1. **Export Mode (primary)**
   - `timeline.json`
   - `keyframes.csv`
   - `effects.json`
   - `captions.srt` (if transcript captions are generated)

2. **Companion Mode**
   - Step-by-step import instructions via `CapCutCompanion`.

3. **Automation Mode (optional)**
   - User confirmation gate.
   - Dry-run mode by default.

## Extensibility

- Plugin registry for:
  - analysis modules
  - style plugins
  - export handlers
- Clear module boundaries under `analysis/`, `decision/`, `timeline/`, `video/`, `integrations/`.

## Monetization-Ready Features

- License policy layer:
  - **Free** tier: style limits + watermark-ready behavior
  - **Pro** tier: full style access and full-resolution policy hooks
- Local-only operation; no cloud dependency required.

## Install

Minimal (lightweight):

```bash
pip install -e .
```

Optional full local model stack:

```bash
pip install -e '.[full]'
```

Dev dependencies:

```bash
pip install -e '.[dev]'
```

## CLI

Batch processing:

```bash
python -m autocut_ai.cli batch input.mp4 --style clean_shorts --out out --license free --intensity 0.7
```

Multi-clip batch:

```bash
python -m autocut_ai.cli batch a.mp4 b.mp4 --style gaming_short --out out_batch
```

Launch terminal UI:

```bash
python -m autocut_ai.cli tui
```

Launch desktop UI:

```bash
python -m autocut_ai.cli desktop
```

## Reliability & Recovery

- Low-confidence warnings when detection/tracking is weak.
- Fallback center-subject framing when models are unavailable.
- Decision traces are included in timeline actions (`reason` field) for debugging.
