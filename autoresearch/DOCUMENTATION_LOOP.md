# Main Loop Integration

This module coordinates the interaction between the Scorer, Refiner, and the experiment log. It implements the batch-mode execution cycle.

## The Loop Cycle
Each iteration of the loop follows these steps:
1. **Selection (Stage C)**: The refiner selects the most promising artifact (or multiple artifacts to merge) from the history.
2. **Merging (Stage M)**: If required, the refiner synthesizes a new base artifact from selected parents.
3. **Diagnosis (Stage A)**: The current parent's failure modes are analyzed to generate a generalization summary.
4. **Proposal (Stage B)**: The refiner generates $K$ sibling candidates based on the parent, the summary, and the shared notebook.
5. **Parallel Scoring**: All $K$ candidates are scored across Train, Dev, and Test splits in parallel.
6. **Logging**: The results of all candidates are appended to the immutable `experiments.jsonl` log.

## Invariants
- **Resumability**: The loop reads the `experiments.jsonl` log at start to reconstruct the history.
- **Crash-Safety**: All writes to the log are append-only and line-buffered.
- **Parallel Throughput**: By scoring $K$ candidates in parallel, the loop achieves a $K\times$ wall-clock speedup over serial execution.
