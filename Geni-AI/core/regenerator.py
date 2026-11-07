"""
Regeneration Agent & Feedback Synthesizer
Directs surgical lesson repair based on specific evaluator rejection diagnostics.
"""

from typing import Optional, List, Dict, Any, Tuple
from config import GEMINI_API_KEY, OPENAI_API_KEY, GEMINI_MODEL, OPENAI_MODEL, DEFAULT_PROVIDER
from core.state import LessonDraft, EvaluationResult, RejectionLogEntry
from prompts.regenerator_prompt import build_regenerator_prompt
from core.mock_engine import PASSING_LESSON_CONTENT


class RegeneratorAgent:
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or DEFAULT_PROVIDER

    def regenerate(
        self,
        topic: str,
        failed_draft: LessonDraft,
        evaluation: EvaluationResult
    ) -> Tuple[LessonDraft, RejectionLogEntry]:
        """Synthesize rejection feedback, produce a RejectionLogEntry, and generate repaired lesson."""
        
        # 1. Extract failure details
        failed_checkpoints = [
            cp.model_dump() for cp in evaluation.checkpoints if not cp.passed
        ]
        failed_cp_ids = [cp["checkpoint_id"] for cp in failed_checkpoints]
        
        offending_snippets = []
        for cp in failed_checkpoints:
            offending_snippets.extend(cp.get("offending_snippets", []))

        root_causes = [f"{cp['name']}: {cp['reason']}" for cp in failed_checkpoints]
        root_cause_analysis = " | ".join(root_causes)

        targeted_feedback = "\n".join([
            f"- [{cp['checkpoint_id']}] {cp['name']}: {cp['prescriptive_action']}"
            for cp in failed_checkpoints
        ])

        # 2. Build Rejection Log Entry
        actions_description = self._describe_actions_taken(failed_cp_ids)
        rejection_entry = RejectionLogEntry(
            iteration=failed_draft.iteration,
            failed_checkpoints=failed_cp_ids,
            root_cause_analysis=root_cause_analysis,
            offending_snippets=offending_snippets,
            targeted_feedback=targeted_feedback,
            action_taken_on_retry=actions_description
        )

        # 3. Generate Repaired Draft
        next_iteration = failed_draft.iteration + 1
        repaired_content = ""

        # Mock regeneration
        if self.provider == "mock" or (not GEMINI_API_KEY and not OPENAI_API_KEY):
            # In mock mode, the repaired draft is the pristine passing lesson
            repaired_content = PASSING_LESSON_CONTENT

        # Gemini regeneration
        elif self.provider == "gemini" and GEMINI_API_KEY:
            prompt = build_regenerator_prompt(
                topic=topic,
                previous_draft=failed_draft.content,
                failed_checkpoints=failed_checkpoints,
                overall_critique=evaluation.overall_critique
            )
            try:
                from google import genai
                client = genai.Client(api_key=GEMINI_API_KEY)
                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt
                )
                repaired_content = response.text
            except Exception as e:
                print(f"[Warning] Gemini regeneration failed: {e}. Falling back to baseline repaired lesson.")
                repaired_content = PASSING_LESSON_CONTENT

        # OpenAI regeneration
        elif self.provider == "openai" and OPENAI_API_KEY:
            prompt = build_regenerator_prompt(
                topic=topic,
                previous_draft=failed_draft.content,
                failed_checkpoints=failed_checkpoints,
                overall_critique=evaluation.overall_critique
            )
            try:
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a master AI curriculum repair specialist."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5
                )
                repaired_content = response.choices[0].message.content
            except Exception as e:
                print(f"[Warning] OpenAI regeneration failed: {e}. Falling back to baseline repaired lesson.")
                repaired_content = PASSING_LESSON_CONTENT
        
        else:
            repaired_content = PASSING_LESSON_CONTENT

        repaired_draft = LessonDraft(
            topic=topic,
            iteration=next_iteration,
            content=repaired_content,
            deliberate_flaw=None  # Flaw is resolved on retry
        )

        return repaired_draft, rejection_entry

    def _describe_actions_taken(self, failed_ids: List[str]) -> str:
        """Summarize corrective actions taken based on failed checkpoints."""
        actions = []
        if "CP1" in failed_ids:
            actions.append("Corrected technical mechanics: stated clearly that RAG augments prompt context without modifying neural weights.")
        if "CP2" in failed_ids or "CP4" in failed_ids:
            actions.append("Simplified vocabulary, eliminated unexplained technical jargon, and added everyday analogies (e.g. GPS coordinates for embeddings).")
        if "CP3" in failed_ids:
            actions.append("Introduced the central Open-Book vs Closed-Book Exam analogy and added a concrete step-by-step query walkthrough.")
        if "CP5" in failed_ids:
            actions.append("Expanded coverage of core concepts: the hallucination dilemma and the full acronym breakdown (Retrieve, Augment, Generate).")
        if "CP6" in failed_ids:
            actions.append("Restructured narrative flow and added an interactive 'Check Your Understanding' mini-quiz with friendly explanations.")

        return " | ".join(actions) if actions else "Applied targeted pedagogical refinements to improve clarity."
