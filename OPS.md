# Operations Guide (OPS)

This document serves as a runbook for AI agents acting as DevOps engineers for the Autoresearch system.

## Deployment and Setup

### Prerequisites
- Python 3.10+
- Necessary LLM API keys configured in the environment.

### Installation
1. Clone the repository.
2. Install dependencies: `pip install numpy`.

### Starting the Loop
To start a research run:
```bash
python loop.py run --artifact "Initial Prompt Text" --dataset "./data/my_dataset" --model "gemma-31b"
```

To run with a limit on iterations:
```bash
python loop.py run --max-iters 10 --artifact "..." --dataset "..."
```

## Environment Variables
| Variable | Description | Example |
|---|---|---|
| `AUTORESEARCH_STATE_DIR` | Overrides the root directory for all state and caches. | `/tmp/run_experiment_1` |

## Health Checks
- **Log Activity**: Verify that `state/experiments.jsonl` is being appended to.
- **Report Growth**: Run `python loop.py report` and check if `state/experiments_report.md` is updating with new iterations.
- **Cache Hits**: Check `state/cache/` to ensure directories are being created for each unique artifact.

## Common Failure Modes
- **LLM Parsing Error**: If the loop stalls or crashes during Stage B/C/M, check the `state/batches/` directory for attempt dumps.
- **Disk Space**: Large datasets and extensive caching can fill disk space. Clear the cache using `python loop.py reset` if necessary.
- **Token Limits**: If the model truncates output, compress the history rendering in `refiner.py`.

## Backup and Restore
- The entire `state/` directory contains all necessary information to resume a run. Backup this directory to preserve the experiment history.
