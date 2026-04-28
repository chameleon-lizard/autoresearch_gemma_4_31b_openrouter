# Dataset Splitter

This module handles the deterministic and stratified splitting of the ground truth dataset into Train, Dev, and Test sets.

## Design
The splitter ensures that the loop's evaluation is robust and resistant to leakage.

- **Stratification**: The `stratified_split` function uses a `domain_key` to ensure that each split (Train, Dev, Test) contains a proportional representation of different domains in the dataset.
- **Determinism**: A fixed seed is used for shuffling, ensuring that the split is reproducible across different runs of the tool.
- **Held-out Test Set**: The Test set is strictly isolated from the loop's proposal and selection stages to detect overfitting to the Dev set.

## Usage
The `stratified_split` function takes a list of dictionaries (the dataset) and returns three lists representing the splits. These can then be persisted to disk using `save_split`.
