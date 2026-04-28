import json
import random
from pathlib import Path
from typing import List, Dict, Any, Tuple
from collections import defaultdict

def stratified_split(
    dataset: List[Dict[str, Any]], 
    domain_key: str, 
    train_ratio: float = 0.4, 
    dev_ratio: float = 0.2, 
    seed: int = 42
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Splits a dataset into train, dev, and test sets, stratified by the given domain key.
    """
    random.seed(seed)
    
    # Group by domain
    domains = defaultdict(list)
    for item in dataset:
        domain = item.get(domain_key, "default")
        domains[domain].append(item)
    
    train_set, dev_set, test_set = [], [], []
    
    for domain, items in domains.items():
        random.shuffle(items)
        n = len(items)
        
        # Calculate split indices
        train_end = int(n * train_ratio)
        dev_end = train_end + int(n * dev_ratio)
        
        train_set.extend(items[:train_end])
        dev_set.extend(items[train_end:dev_end])
        test_set.extend(items[dev_end:])
        
    return train_set, dev_set, test_set

def save_split(
    train: List[Dict[str, Any]], 
    dev: List[Dict[str, Any]], 
    test: List[Dict[str, Any]], 
    output_dir: Path
):
    """Saves the split datasets to JSONL files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for name, data in [("train", train), ("dev", dev), ("test", test)]:
        with open(output_dir / f"{name}.jsonl", "w") as f:
            for item in data:
                f.write(json.dumps(item) + "\n")

def load_dataset(path: Path) -> List[Dict[str, Any]]:
    """Loads a JSONL dataset."""
    dataset = []
    with open(path, "r") as f:
        for line in f:
            dataset.append(json.loads(line))
    return dataset
