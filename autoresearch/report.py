import json
from pathlib import Path
from typing import List, Dict, Any
from autoresearch.paths import EXPERIMENTS_LOG, EXPERIMENTS_REPORT

def generate_report():
    """
    Regenerates experiments_report.md from the experiments.jsonl log.
    """
    if not EXPERIMENTS_LOG.exists():
        print("No experiments log found.")
        return

    history = []
    with open(EXPERIMENTS_LOG, "r") as f:
        for line in f:
            history.append(json.loads(line))
    
    # Sort by iteration
    history.sort(key=lambda x: x.get("iter", 0))
    
    # Find best
    best = max(history, key=lambda x: x["metrics_dev"]["kappa"])
    
    report = f"# Autoresearch Experiments Report\n\n"
    report += f"**Best Iteration**: {best['iter']} (Dev Kappa: {best['metrics_dev']['kappa']:.4f})\n\n"
    
    report += "## Iteration Log\n\n"
    report += "| Iter | Parent | Plan ID | Dev Kappa | Test Kappa | Rationale |\n"
    report += "|---|---|---|---|---|---|\n"
    
    for entry in history:
        report += f"| {entry['iter']} | {entry['parent']} | {entry.get('plan_id', 'N/A')} | {entry['metrics_dev']['kappa']:.4f} | {entry['metrics_test']['kappa']:.4f} | {entry['rationale']} |\n"
    
    EXPERIMENTS_REPORT.write_text(report)
    print(f"Report generated at {EXPERIMENTS_REPORT}")
