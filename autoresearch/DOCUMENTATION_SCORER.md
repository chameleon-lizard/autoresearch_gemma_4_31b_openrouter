# Scorer Driver

This module manages the execution of the scoring process. It acts as a wrapper around an external scorer CLI tool, adhering to the design principle of "Wrap, don't reimplement."

## Design
- **Subprocess Wrapping**: The driver calls an external CLI (e.g., `dredd.py`). This allows the system to inherit the CLI's internal caching, A/B swap logic, and retry mechanisms.
- **Parallel Execution**: The `score_batch` method uses a `ThreadPoolExecutor` to score multiple candidates in parallel, providing a $K \times$ speedup in throughput.
- **Cache Integration**: Before calling the CLI, the driver checks the content-hash cache. If a result exists for the artifact and the specific dataset split, it is returned immediately.
- **Self-Describing Cache**: Every new artifact scored is saved to `state/cache/<hash>/artifact.txt`.

## Implementation Details
- `score_artifact`: The primary entry point for single artifact evaluation.
- `score_batch`: The entry point for batch evaluation of sibling candidates.
- `_run_scorer_cli`: Handles the actual subprocess communication and output parsing.
