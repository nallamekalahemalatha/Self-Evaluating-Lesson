"""
Self-Evolution Engine
Analyzes failure patterns across runs to synthesize dynamic prompt guardrails.
"""

import json
from typing import List, Dict, Any
from pathlib import Path
from config import EVOLUTION_STORE_PATH
from core.state import RejectionLogEntry


DEFAULT_GUARDRAILS = [
    "Always define 'Vector' or 'Embedding' immediately as 'a numerical address/tag that stores meaning, just like a pin on Google Maps'.",
    "Never use the term 'Retrieval' without immediately giving the synonym 'Searching/Fetching the right page from a book'.",
    "Explicitly emphasize that RAG does NOT update AI model weights or retrain the neural network; it gives fresh context in the prompt note.",
    "Keep every sentence short and punchy: break sentences with more than one 'and/which/because' into two separate sentences.",
    "Always feature a relatable Indian student analogy (e.g. Open-Book vs Closed-Book exam) in the first 2 sections."
]


class EvolutionEngine:
    def __init__(self, store_path: Path = EVOLUTION_STORE_PATH):
        self.store_path = store_path
        self._ensure_store()

    def _ensure_store(self):
        """Initialize evolution store if it does not exist."""
        if not self.store_path.exists():
            data = {
                "active_guardrails": list(DEFAULT_GUARDRAILS),
                "evolution_history": [
                    {
                        "source": "Seed Calibration",
                        "synthesized_guardrail": g,
                        "timestamp": "initial"
                    } for g in DEFAULT_GUARDRAILS
                ]
            }
            self.store_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.store_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

    def get_active_guardrails(self) -> List[str]:
        """Fetch current evolved guardrails to inject into generator prompts."""
        self._ensure_store()
        try:
            with open(self.store_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("active_guardrails", DEFAULT_GUARDRAILS)
        except Exception:
            return DEFAULT_GUARDRAILS

    def evolve_from_rejections(self, rejections: List[RejectionLogEntry]) -> List[str]:
        """
        Analyze new rejections from a pipeline run and synthesize new guardrails.
        Returns newly added guardrails.
        """
        if not rejections:
            return []

        self._ensure_store()
        with open(self.store_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        existing_guardrails = set(data.get("active_guardrails", []))
        newly_added = []

        for rj in rejections:
            for cp_id in rj.failed_checkpoints:
                derived_rule = None
                
                if cp_id == "CP1":
                    derived_rule = "Strict Fact-Check Rule: State explicitly that RAG does not retrain weights, but provides real-time reference notes to the AI prompt."
                elif cp_id == "CP2":
                    derived_rule = "Simplification Rule: Ensure sentence length remains under 16 words and avoid passive academic terminology."
                elif cp_id == "CP3":
                    derived_rule = "Pedagogical Anchor Rule: Include both the Open-Book Exam analogy AND a concrete step-by-step query walkthrough."
                elif cp_id == "CP4":
                    derived_rule = f"Jargon Ban Rule: Ensure terms like {', '.join(rj.offending_snippets[:2]) or 'technical acronyms'} are accompanied by 'in simple words' definitions."
                elif cp_id == "CP5":
                    derived_rule = "Completeness Rule: Explicitly unpack all 3 steps: R (Retrieve), A (Augment), G (Generate) in distinct bullet points."
                elif cp_id == "CP6":
                    derived_rule = "Interactive Closure Rule: Conclude with an active 'Check Your Understanding' mini-quiz with 2-3 questions and friendly answer rationales."

                if derived_rule and derived_rule not in existing_guardrails:
                    existing_guardrails.add(derived_rule)
                    newly_added.append(derived_rule)
                    data.setdefault("evolution_history", []).append({
                        "source": f"Rejection in iteration {rj.iteration}",
                        "failed_checkpoint": cp_id,
                        "synthesized_guardrail": derived_rule,
                        "timestamp": rj.timestamp
                    })

        if newly_added:
            data["active_guardrails"] = list(existing_guardrails)
            with open(self.store_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

        return newly_added
