import os
from pathlib import Path

# Default state directory if not provided by env var
DEFAULT_STATE_DIR = Path("./state")

# Root state directory
STATE_DIR = Path(os.environ.get("AUTORESEARCH_STATE_DIR", DEFAULT_STATE_DIR))

# Core directories
CACHE_DIR = STATE_DIR / "cache"
ITERATIONS_DIR = STATE_DIR / "iterations"
BATCHES_DIR = STATE_DIR / "batches"

# Core files
EXPERIMENTS_LOG = STATE_DIR / "experiments.jsonl"
EXPERIMENTS_REPORT = STATE_DIR / "experiments_report.md"
NOTES_FILE = STATE_DIR / "notes.md"

def ensure_dirs():
    """Ensure all required state directories exist."""
    for directory in [STATE_DIR, CACHE_DIR, ITERATIONS_DIR, BATCHES_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

def get_artifact_cache_dir(artifact_hash: str) -> Path:
    """Get the specific cache directory for a given artifact hash."""
    return CACHE_DIR / artifact_hash
