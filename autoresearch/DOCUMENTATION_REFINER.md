# Refiner

This module implements the core LLM-driven logic for evolving artifacts. It consists of four distinct stages (A, B, C, and M), each with a specific cognitive task.

## Refiner Stages

### Stage A: Disagreement Generalisation
- **Goal**: Prevent overfitting to specific examples.
- **Process**: Takes a sample of errors and produces a high-level abstraction of the failure mode.
- **Output**: A free-text summary of *why* the artifact is failing.

### Stage B: Proposal
- **Goal**: Generate focused mutations.
- **Process**: Uses the parent artifact, the Stage-A summary, and a compact history to propose $K$ sibling candidates.
- **Invariant**: Each candidate must apply exactly one focused edit (Single-edit attribution).

### Stage C: Selection
- **Goal**: Choose the next base for evolution.
- **Process**: Analyzes the history of metrics and trajectories.
- **Output**: Either selects a single iteration as the parent or identifies multiple candidates for merging.

### Stage M: Merge Synthesis
- **Goal**: Combine promising lineages.
- **Process**: Synthesizes a new base artifact that integrates the best parts of multiple parents.

## LLM Interaction
The refiner uses a retry loop with a stochastic temperature schedule `[0.0, 0.4, 0.7, 0.9]` to handle parsing failures without producing identical outputs.
