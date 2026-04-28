import hashlib
from pathlib import Path
import json
from typing import Any, Optional
from autoresearch.paths import get_artifact_cache_dir

def compute_artifact_hash(artifact: str) -> str:
    """
    Compute a deterministic 16-character SHA-256 hash of the artifact content.
    """
    return hashlib.sha256(artifact.encode("utf-8")).hexdigest()[:16]

def cache_result(artifact_hash: str, key: str, value: Any):
    """
    Caches a result for a given artifact and key in the artifact's cache directory.
    """
    cache_dir = get_artifact_cache_dir(artifact_hash)
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    with open(cache_dir / f"{key}.json", "w") as f:
        json.dump(value, f)

def get_cached_result(artifact_hash: str, key: str) -> Optional[Any]:
    """
    Retrieves a cached result for a given artifact and key.
    """
    cache_dir = get_artifact_cache_dir(artifact_hash)
    cache_file = cache_dir / f"{key}.json"
    
    if not cache_file.exists():
        return None
    
    with open(cache_file, "r") as f:
        return json.load(f)

def cache_artifact_text(artifact_hash: str, text: str):
    """
    Stores the original artifact text in the cache directory for self-description.
    """
    cache_dir = get_artifact_cache_dir(artifact_hash)
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    with open(cache_dir / "artifact.txt", "w") as f:
        f.write(text)
