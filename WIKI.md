# Autoresearch Loops Wiki

## Overview
Autoresearch Loops is a framework for the autonomous optimization of LLM artifacts (such as prompts, configurations, or code patches). It uses a closed-loop system where an LLM analyzes failures, proposes mutations, and selects the best candidates based on metrics from a held-out evaluation set.

## Core Architecture
The system operates in a loop consisting of four primary stages:
- **Stage A (Diagnose)**: Analyzes disagreements between the current artifact and ground truth to generate a high-level generalization of failure modes.
- **Stage B (Propose)**: Generates $K$ sibling candidates, each applying a single focused edit to a parent artifact.
- **Stage C (Select)**: Chooses the best candidate or decides to merge multiple promising lineages to serve as the next parent.
- **Stage M (Merge)**: Synthesizes a new base artifact from multiple parents.

## Key Invariants
- **Content-Hash Caching**: Every artifact is identified by the SHA-256 hash of its content. Results of scoring and diagnosis are cached by this hash to avoid redundant work.
- **Immutable Log**: All iterations are recorded in an append-only `experiments.jsonl` file.
- **Dataset Splitting**: The dataset is split into Train, Dev, and Test sets. The loop optimizes for Dev, while Test remains untouched to detect overfitting.
- **Single-Edit Attribution**: Only one focused change per candidate is allowed to ensure clear attribution of metric changes.
- **Bi-directional Notebook**: A shared `notes.md` file allows for human intervention and agent observations.

## File Structure
- `autoresearch/`: Core implementation.
  - `splitter.py`: Handles dataset splitting.
  - `scorer.py`: Manages the scoring process and caching.
  - `metrics.py`: Calculates success metrics.
  - `refiner.py`: Implements Stages A, B, C, and M.
  - `loop.py`: The main execution loop.
  - `report.py`: Generates the experiment report.
  - `paths.py`: Centralized path and configuration management.
- `state/`: Persistent storage (configurable via `AUTORESEARCH_STATE_DIR`).
  - `cache/`: Hashed results of artifact evaluations.
  - `iterations/`: Log of loop iterations.
  - `batches/`: Detailed data for each batch of proposals.
