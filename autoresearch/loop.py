import json
import time
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from autoresearch.paths import *
from autoresearch.cache import compute_artifact_hash
from autoresearch.scorer import ScorerDriver
from autoresearch.refiner import Refiner
from autoresearch.metrics import calculate_metrics

class AutoresearchLoop:
    def __init__(self, 
                 initial_artifact: str, 
                 dataset_dir: Path, 
                 scorer_cli: str, 
                 model_name: str, 
                 k_siblings: int = 3):
        self.initial_artifact = initial_artifact
        self.dataset_dir = dataset_dir
        self.scorer = ScorerDriver(scorer_cli, dataset_dir)
        self.refiner = Refiner(model_name)
        self.k_siblings = k_siblings
        
        ensure_dirs()

    def _log_iteration(self, data: Dict[str, Any]):
        with open(EXPERIMENTS_LOG, "a") as f:
            f.write(json.dumps(data) + "\n")

    def _get_history(self) -> List[Dict[str, Any]]:
        if not EXPERIMENTS_LOG.exists():
            return []
        history = []
        with open(EXPERIMENTS_LOG, "r") as f:
            for line in f:
                history.append(json.loads(line))
        return history

    def _get_best_artifact(self) -> Tuple[int, str]:
        history = self._get_history()
        if not history:
            return 0, self.initial_artifact
        
        # Find iteration with max dev kappa
        best_iter = max(history, key=lambda x: x["metrics_dev"]["kappa"])
        # We need to retrieve the artifact text from cache
        artifact_hash = best_iter["artifact_hash"]
        with open(CACHE_DIR / artifact_hash / "artifact.txt", "r") as f:
            return best_iter["iter"], f.read()

    def run(self, max_iters: Optional[int] = None):
        current_iter = 0
        
        # Initial scoring
        parent_text = self.initial_artifact
        parent_hash = compute_artifact_hash(parent_text)
        
        # Initial metrics
        m_train = self.scorer.score_artifact(parent_text, "train")
        m_dev = self.scorer.score_artifact(parent_text, "dev")
        m_test = self.scorer.score_artifact(parent_text, "test")
        
        self._log_iteration({
            "iter": current_iter,
            "ts": time.time(),
            "artifact_hash": parent_hash,
            "parent": None,
            "metrics_train": m_train,
            "metrics_dev": m_dev,
            "metrics_test": m_test,
            "rationale": "Initial Artifact"
        })
        
        while True:
            if max_iters and current_iter >= max_iters:
                break
            
            current_iter += 1
            
            # 1. Stage C: Select Parent
            history = self._get_history()
            best_id, best_text = self._get_best_artifact()
            selection = self.refiner.stage_c_select(history, {"id": best_id, "text": best_text})
            
            if selection["selection"] == "single":
                # Need to find the artifact text for the selected ID
                # In a real implementation, we'd map ID -> Hash -> Text
                parent_text = best_text 
            else:
                # Stage M: Merge
                parent_texts = [best_text] # Simplified for mock
                parent_text = self.refiner.stage_m_merge(parent_texts)
            
            # 2. Stage A: Diagnose
            # Use errors from the parent's dev score
            parent_hash = compute_artifact_hash(parent_text)
            dev_results = self.scorer.score_artifact(parent_text, "dev")
            summary = self.refiner.stage_a_diagnose(parent_text, dev_results.get("errors", []))
            
            # 3. Stage B: Propose
            notebook_text = NOTES_FILE.read_text() if NOTES_FILE.exists() else ""
            proposals = self.refiner.stage_b_propose(parent_text, summary, str(history), notebook_text, self.k_siblings)
            
            # 4. Score Siblings in Parallel
            batch_artifacts = [p["artifact"] for p in proposals]
            train_scores = self.scorer.score_batch(batch_artifacts, "train")
            dev_scores = self.scorer.score_batch(batch_artifacts, "dev")
            test_scores = self.scorer.score_batch(batch_artifacts, "test")
            
            # 5. Log Results
            for i, proposal in enumerate(proposals):
                art_hash = compute_artifact_hash(proposal["artifact"])
                self._log_iteration({
                    "iter": current_iter * 10 + i, # Simplified ID
                    "ts": time.time(),
                    "artifact_hash": art_hash,
                    "parent": parent_hash,
                    "plan_id": proposal["plan_id"],
                    "rationale": proposal["rationale"],
                    "metrics_train": train_scores[i],
                    "metrics_dev": dev_scores[i],
                    "metrics_test": test_scores[i],
                })
                
            print(f"Completed iteration {current_iter} with {self.k_siblings} candidates.")

    def stop(self):
        print("Stopping loop...")
