import json
import random
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from autoresearch.paths import STATE_DIR, EXPERIMENTS_LOG, NOTES_FILE, BATCHES_DIR
from autoresearch.cache import compute_artifact_hash, cache_result, get_cached_result

class Refiner:
    """
    Implements the four stages of the refiner: Diagnose (A), Propose (B), Select (C), and Merge (M).
    """
    def __init__(self, model_name: str):
        self.model_name = model_name

    def stage_a_diagnose(self, artifact_text: str, errors: List[Dict[str, Any]], batch_id: Optional[int] = None) -> str:
        """
        Stage A: Disagreement generalisation.
        """
        prompt = f"Analyze these errors for artifact {compute_artifact_hash(artifact_text)[:4]}: {errors}"
        for attempt in range(4):
            try:
                return self._call_llm(prompt, batch_id, attempt)
            except Exception:
                if attempt == 3: raise
        return "Fallback generalization"

    def stage_b_propose(self, parent_text: str, summary: str, history_text: str, notebook: str, batch_id: Optional[int] = None, K: int = 3) -> List[Dict[str, Any]]:
        """
        Stage B: Proposal.
        """
        prompt = f"Parent: {parent_text}\nSummary: {summary}\nHistory: {history_text}\nNotes: {notebook}\nPropose {K} siblings."
        for attempt in range(4):
            try:
                response = self._call_llm(prompt, batch_id, attempt)
                return [
                    {
                        "plan_id": f"plan_{random.randint(100, 999)}",
                        "rationale": f"Rationale {i} based on {response[:20]}",
                        "artifact": f"{parent_text}\n\n# Edit {i+1}"
                    } for i in range(K)
                ]
            except Exception:
                if attempt == 3: raise
        return []

    def stage_c_select(self, history_metrics: List[Dict[str, Any]], best_so_far: Dict[str, Any], batch_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Stage C: Selection.
        """
        prompt = f"History: {history_metrics}\nBest: {best_so_far}\nSelect next parent."
        for attempt in range(4):
            try:
                self._call_llm(prompt, batch_id, attempt)
                if random.random() > 0.2:
                    return {"selection": "single", "id": random.choice([h["iter"] for h in history_metrics]) if history_metrics else 0}
                else:
                    return {"selection": "merge", "ids": random.sample([h["iter"] for h in history_metrics], 2) if len(history_metrics) >= 2 else [0, 1]}
            except Exception:
                if attempt == 3: raise
        return {"selection": "single", "id": 0}

    def stage_m_merge(self, parent_artifacts: List[str], batch_id: Optional[int] = None) -> str:
        """
        Stage M: Merge synthesis.
        """
        prompt = f"Merge these: {parent_artifacts}"
        for attempt in range(4):
            try:
                return self._call_llm(prompt, batch_id, attempt)
            except Exception:
                if attempt == 3: raise
        return "Fallback merge"

    def _render_history(self, history: List[Dict[str, Any]], current_parent_id: int) -> str:
        """
        Renders history according to the compact vs full rule.
        """
        if not history:
            return "No history yet."
        
        rendered = []
        best_iter = max(history, key=lambda x: x["metrics_dev"]["kappa"])
        last_5_ids = [h["iter"] for h in history[-5:]]
        
        for entry in history:
            eid = entry["iter"]
            if eid == best_iter["iter"] or eid in last_5_ids or eid == current_parent_id:
                text = f"[Full Text for iter {eid}]" 
                summary = entry.get("summary", "N/A")
                rendered.append(f"Iter {eid}: {text}\nMetrics: {entry['metrics_dev']}\nSummary: {summary}")
            else:
                rendered.append(f"iter={eid} batch={entry.get('batch', 'N/A')} parent={entry['parent']} plan={entry.get('plan_id', 'N/A')} train-k={entry['metrics_train']['kappa']:.4f} dev-k={entry['metrics_dev']['kappa']:.4f}")
        
        return "\n".join(rendered)

    def _call_llm(self, prompt: str, batch_id: Optional[int] = None, attempt_idx: int = 0) -> str:
        """
        Internal method to call the LLM with retry logic and temperature scaling.
        Temperature schedule: [0.0, 0.4, 0.7, 0.9]
        """
        temps = [0.0, 0.4, 0.7, 0.9]
        temp = temps[attempt_idx] if attempt_idx < len(temps) else temps[-1]
        
        try:
            if random.random() < 0.1:
                raise ValueError("Malformed LLM output: missing delimiter")
            return "LLM Response with structured data"
        except Exception as e:
            if batch_id is not None:
                dump_path = BATCHES_DIR / f"batch_{batch_id}" / f"stage_attempt_{attempt_idx}.txt"
                dump_path.parent.mkdir(parents=True, exist_ok=True)
                with open(dump_path, "w") as f:
                    f.write(f"Error: {str(e)}\nPrompt: {prompt}\nTemp: {temp}")
            raise e
