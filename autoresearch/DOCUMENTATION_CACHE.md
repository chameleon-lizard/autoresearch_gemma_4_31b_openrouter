# Artifact Caching

This module implements the content-hash caching invariant, ensuring that expensive operations like scoring and diagnosis are never repeated for the same artifact.

## Design
- **Deterministic Hashing**: Artifacts are identified by a 16-character prefix of their SHA-256 hash. This hash is derived solely from the artifact's functional content.
- **Self-Describing Cache**: The original artifact text is stored alongside the results in `state/cache/<hash>/artifact.txt`.
- **Key-Value Storage**: Results are stored as JSON files within the artifact's specific cache directory, where the filename corresponds to the `key` (e.g., `scoring.json`, `diagnosis.json`).

## Invariants
1. **No Redundant Work**: A re-run of the loop must never redo work it has already done if the artifact hash is present in the cache.
2. **Content-Only Keys**: Non-functional state (timestamps, run IDs) is excluded from the hash input.
