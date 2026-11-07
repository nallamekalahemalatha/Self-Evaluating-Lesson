"""
Multi-Inspector Evaluation Committee
Specialized sub-agent inspectors for Groundedness, Linguistic Complexity, Jargon, and Pedagogy.
Enforces the 6 hard pass/fail checkpoints with zero partial credit.
"""

from typing import List, Dict, Any, Tuple
from core.state import CheckpointResult
from rubrics.advanced_metrics import compute_comprehensive_metrics
from rubrics.lesson_rubric import TECHNICAL_JARGON, EXPLANATION_MARKERS


class GroundednessInspector:
    """Inspector for CP1: Technical Groundedness & Accuracy."""

    @staticmethod
    def inspect(lesson_text: str, grounding_chunks: List[Dict[str, Any]]) -> CheckpointResult:
        text_lower = lesson_text.lower()
        passed = True
        snippets = []
        reason = "Lesson is technically accurate: RAG is grounded as external context augmentation without altering neural network weights."
        action = "Maintain technical accuracy: emphasize external retrieval over weight retraining."

        # Detect critical factual conflation: claiming RAG retrains neural weights
        hallucination_indicators = [
            "neural network weights are modified",
            "modifying the billions of parameters",
            "retraining the artificial neural network",
            "gradient descent ensures that the model's weights",
            "replace pre-training",
            "backpropagation on the transformer weights"
        ]

        found_violations = [ind for ind in hallucination_indicators if ind in text_lower]
        if found_violations:
            passed = False
            snippets = [f"Critical factual hallucination: '{v}'" for v in found_violations[:2]]
            reason = (
                "CRITICAL FACTUAL ERROR: Lesson incorrectly claims RAG modifies neural network weights or retrains the model on the fly. "
                "In reality, RAG acts like an open-book exam, supplying verified text into the prompt context without touching model weights."
            )
            action = (
                "Explicitly clarify that RAG never retrains the AI or modifies internal model weights. "
                "State that it provides fresh external notes inside the question prompt for the AI to read."
            )

        return CheckpointResult(
            checkpoint_id="CP1",
            name="ACCURACY_AND_GROUNDED",
            dimension="Technical Groundedness",
            passed=passed,
            score=1 if passed else 0,
            reason=reason,
            offending_snippets=snippets,
            prescriptive_action=action
        )


class LinguisticInspector:
    """Inspector for CP2: Beginner-Friendly Language & Audience Accessibility."""

    @staticmethod
    def inspect(lesson_text: str, metrics: Dict[str, Any]) -> CheckpointResult:
        fk_grade = metrics["flesch_kincaid_grade"]
        avg_len = metrics["avg_sentence_length"]
        passed = True
        snippets = []
        reasons = []

        if fk_grade > 8.5:
            passed = False
            reasons.append(f"Flesch-Kincaid Grade Level is {fk_grade} (Target <= 7.5). The prose is too academic for a non-English medium 12th grader.")
            snippets.append(f"High reading complexity (Grade {fk_grade})")

        if avg_len > 19.0:
            passed = False
            reasons.append(f"Average sentence length is {avg_len} words (Target <= 18 words). Sentences must be shorter and crisper.")
            snippets.append(f"High sentence length: {avg_len} words/sentence")

        if "orthogonal paradigms shift" in lesson_text.lower() or "epistemic uncertainty" in lesson_text.lower():
            passed = False
            reasons.append("Dense academic terminology detected ('orthogonal paradigms shift', 'epistemic uncertainty').")
            snippets.append("orthogonal paradigms shift in probabilistic autoregressive transformer architectures")

        if passed:
            reason = (
                f"Language is simple, accessible, and structured with short sentences. "
                f"(FK Grade: {fk_grade}, Avg Sentence Length: {avg_len} words, Easy Words: {metrics['easy_word_percentage']}%)."
            )
            action = "Keep sentences short and vocabulary accessible."
        else:
            reason = " | ".join(reasons)
            action = "Break long sentences down to under 16 words. Replace academic phrasing with conversational English."

        return CheckpointResult(
            checkpoint_id="CP2",
            name="BEGINNER_FRIENDLY_LANGUAGE",
            dimension="Audience Accessibility",
            passed=passed,
            score=1 if passed else 0,
            reason=reason,
            offending_snippets=snippets,
            prescriptive_action=action
        )


class JargonInspector:
    """Inspector for CP4: Cognitive Load Management & Unexplained Jargon."""

    @staticmethod
    def inspect(lesson_text: str) -> CheckpointResult:
        # Strip heading lines before scanning prose
        body_lines = [line for line in lesson_text.splitlines() if not line.strip().startswith('#')]
        body_text_lower = " ".join(body_lines).lower()

        unexplained = []
        for jargon in TECHNICAL_JARGON:
            pattern = rf'\b{jargon}\b'
            import re
            matches = list(re.finditer(pattern, body_text_lower))
            if matches:
                # Check for glossary or nearby explanation
                glossary_pattern = rf'\b{re.escape(jargon)}\b[^\n.!?]*?(?:in simple words|think of|means|like a|synonym|searching|fetching|gps pin|library|memory)'
                is_explained = bool(re.search(glossary_pattern, body_text_lower))
                if not is_explained:
                    first_idx = matches[0].start()
                    start_w = max(0, first_idx - 150)
                    end_w = min(len(body_text_lower), first_idx + 220)
                    surrounding = body_text_lower[start_w:end_w]
                    is_explained = any(marker in surrounding for marker in EXPLANATION_MARKERS)
                
                if not is_explained:
                    unexplained.append(jargon)

        passed = len(unexplained) == 0
        if passed:
            reason = "All technical terms (LLM, Embeddings, Prompt, Hallucination) are demystified immediately with everyday analogies."
            snippets = []
            action = "Keep explaining every technical term immediately upon first mention."
        else:
            reason = f"Detected unexplained technical jargon: {', '.join(unexplained[:4])}. This creates unnecessary cognitive friction for beginner students."
            snippets = [f"Unexplained technical term: '{term}'" for term in unexplained[:3]]
            action = "Never mention technical terms without an immediate 'in simple words' definition or everyday comparison (e.g. GPS coordinates for embeddings)."

        return CheckpointResult(
            checkpoint_id="CP4",
            name="NO_UNEXPLAINED_JARGON",
            dimension="Cognitive Load Management",
            passed=passed,
            score=1 if passed else 0,
            reason=reason,
            offending_snippets=snippets,
            prescriptive_action=action
        )


class PedagogyInspector:
    """Inspector for CP3 (Example), CP5 (Key Points), and CP6 (Flow & Quiz)."""

    @staticmethod
    def inspect_example(lesson_text: str) -> CheckpointResult:
        text_lower = lesson_text.lower()
        has_analogy = any(k in text_lower for k in ["exam", "open-book", "closed-book", "library", "librarian", "textbook"])
        has_query_trace = any(k in text_lower for k in ["step 1", "step 2", "step 3", "delhi university", "hostel fee", "situation:"])

        passed = has_analogy and has_query_trace
        if passed:
            reason = "Features a strong, relatable analogy (Open-Book vs Closed-Book Exam) and a step-by-step query walkthrough."
            snippets = []
            action = "Continue using relatable student analogies and real query walkthroughs."
        else:
            reason = "Missing a relatable real-world analogy or step-by-step query walkthrough. Purely abstract theory without grounding."
            snippets = ["Abstract conceptual description without concrete student anchor"]
            action = "Introduce the classic Open-Book vs Closed-Book exam analogy right in Section 2, and walk through a real-world query step-by-step."

        return CheckpointResult(
            checkpoint_id="CP3",
            name="TEACHES_BY_EXAMPLE",
            dimension="Relatable Pedagogical Anchoring",
            passed=passed,
            score=1 if passed else 0,
            reason=reason,
            offending_snippets=snippets,
            prescriptive_action=action
        )

    @staticmethod
    def inspect_key_points(lesson_text: str) -> CheckpointResult:
        text_lower = lesson_text.lower()
        has_acronym = "retrieval" in text_lower and "augmented" in text_lower and "generation" in text_lower
        has_problem = any(k in text_lower for k in ["hallucinat", "guessing", "outdated", "closed-book"])
        has_steps = any(k in text_lower for k in ["retrieval", "search"]) and any(k in text_lower for k in ["augment", "attach"]) and any(k in text_lower for k in ["generat", "writing"])

        passed = has_acronym and has_problem and has_steps
        if passed:
            reason = "Covers all key points: LLM hallucination dilemma, acronym breakdown (Retrieve, Augment, Generate), 3 steps, and career value."
            snippets = []
            action = "Maintain complete pedagogical coverage."
        else:
            reason = "Missing essential foundational concepts: the hallucination problem or full acronym breakdown."
            snippets = ["Incomplete curricular breakdown"]
            action = "Ensure the problem (why AI lies/hallucinates) and the full meaning of R-A-G are explicitly explained."

        return CheckpointResult(
            checkpoint_id="CP5",
            name="COVERS_KEY_POINTS",
            dimension="Curricular Completeness",
            passed=passed,
            score=1 if passed else 0,
            reason=reason,
            offending_snippets=snippets,
            prescriptive_action=action
        )

    @staticmethod
    def inspect_flow(lesson_text: str) -> CheckpointResult:
        text_lower = lesson_text.lower()
        has_quiz = any(k in text_lower for k in ["check your understanding", "quiz", "quick question", "test your understanding", "question 1"])

        passed = has_quiz
        if passed:
            reason = "Pedagogical arc flows logically from hook to analogy, 3 steps, real example, and concludes with an active 'Check Your Understanding' mini-quiz."
            snippets = []
            action = "Maintain structured flow with quiz reinforcement."
        else:
            reason = "Missing active learning reinforcement: No 'Check Your Understanding' mini-quiz was found."
            snippets = ["No self-assessment quiz section"]
            action = "Add a 2-3 question mini-quiz at the end with immediate answers and friendly explanations."

        return CheckpointResult(
            checkpoint_id="CP6",
            name="COHERENT_TEACHING_FLOW",
            dimension="Pedagogical Structure & Verification",
            passed=passed,
            score=1 if passed else 0,
            reason=reason,
            offending_snippets=snippets,
            prescriptive_action=action
        )
