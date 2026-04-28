# Paths and Configuration

This module handles all path management and environment configuration for the Autoresearch system.

## Key Features
- **Environment Variable Support**: The root state directory can be overridden via `AUTORESEARCH_STATE_DIR`.
- **Centralized Pathing**: All file and directory locations are derived from `STATE_DIR` to ensure multi-instance support.
- **Automatic Directory Creation**: `ensure_dirs()` handles the setup of the required folder structure.

## Directory Structure
- `state/cache/`: Stores results of scoring and diagnosis keyed by artifact hash.
- `state/iterations/`: Stores metadata for individual iterations.
- `state/batches/`: Stores detailed data for proposal batches.
- `state/experiments.jsonl`: The ground-truth append-only log of all experiments.
- `state/experiments_report.md`: The generated summary report.
- `state/notes.md`: The bi-directional notebook for human-agent communication.
