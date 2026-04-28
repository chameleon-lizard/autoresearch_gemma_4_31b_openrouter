# Report Generator

This module provides the ability to generate a human-readable summary of the experiment's progress.

## Design
- **Deterministic Generation**: The report is entirely derived from the `experiments.jsonl` log. It can be regenerated at any time without loss of information.
- **Provenance**: The report tracks the lineage of each artifact (parent hash), the specific plan used for mutation, and the resulting metrics.
- **Overfit Detection**: By displaying both Dev and Test metrics side-by-side, the report allows the user to visually detect when the Dev-Test gap begins to diverge.

## Usage
The `generate_report()` function reads the immutable log and writes a Markdown table to `experiments_report.md`.
