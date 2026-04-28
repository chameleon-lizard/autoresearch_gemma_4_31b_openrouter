# Metrics Module

This module is responsible for calculating the success signals used by the selector to evaluate artifacts.

## Design
To avoid brittleness, the system tracks multiple correlated metrics instead of a single one:
- **Cohen's Kappa ($\kappa$)**: Measures inter-rater agreement, accounting for chance.
- **Macro-F1**: Ensures performance is balanced across all classes.
- **Spearman's Rho**: Measures the rank correlation between predicted and ground truth values.

## Invariants
- **Verification**: The metrics implementation must be verified against a reference implementation byte-for-byte to ensure correctness.
- **Joint Maximisation**: The selector is prompted to jointly maximise these metrics, preventing it from exploiting pathologies in a single metric.
