"""
High-Fidelity Mock Engine
Provides zero-API-key simulation for testing, evaluation, and Loom video demonstrations.
Includes realistic draft generations, deliberate flaws, and verified passing lessons.
"""

from typing import Dict, Any, List
from core.state import EvaluationResult, CheckpointResult, ReadabilityStats
from rubrics.lesson_rubric import analyze_readability
from core.curriculum import COMPREHENSIVE_RAG_LESSON


# Flagship verified comprehensive RAG curriculum lesson
PASSING_LESSON_CONTENT = COMPREHENSIVE_RAG_LESSON

# Flawed draft 1: Dense unexplained academic jargon
FLAWED_JARGON_CONTENT = """# Introduction to RAG Systems
A Treatise on Non-Parametric Memory Architectures for High-Dimensional Latent Spaces

Retrieval-Augmented Generation constitutes an orthogonal paradigms shift in probabilistic autoregressive transformer architectures. In conventional feed-forward generation, stochastic inference relies exclusively on parametric weights derived during backpropagation over static pre-training corpora. Consequently, epistemic uncertainty precipitates stochastic hallucinations whenever out-of-distribution prompts intercept latency bounds.

To mitigate parametric drift, RAG implements dense vector indexing via bi-encoder dual-tower encoders. Source documents undergo recursive tokenization and are projected into a non-Euclidean manifold using contrastive loss embeddings. During inference, the query vector is transformed via inner-product matrix multiplication to compute cosine similarity scores over HNSW indices.

The retrieved k-nearest neighbors are concatenated into the prompt tensor within the attention context window. The cross-attention layers then modulate next-token softmax probabilities, attenuating hallucination through contextual grounding.

### Architectural Nuances
- Dense Passage Retrieval (DPR) utilizing BERT-base bi-encoders.
- FAISS index structures with Voronoi cell quantization.
- Softmax cross-entropy minimization across generative sequences.
"""

# Flawed draft 2: Factual hallucination / weights retraining error
FLAWED_HALLUCINATION_CONTENT = """# Introduction to RAG (Retrieval-Augmented Generation)

In this lesson, we will explore RAG. RAG stands for Retrieval-Augmented Generation.

When an AI model does not know an answer, it needs to be updated. Standard AI models are static and cannot learn. RAG solves this problem by retraining the artificial neural network on the fly. 

Whenever a user submits a query to a RAG pipeline, the retrieval engine fetches documents from the internet and initiates an automated fine-tuning cycle. The internal neural network weights of the LLM are modified directly, updating the billions of parameters inside the model's brain to permanently encode the new facts. This continuous gradient descent ensures that the model's weights permanently remember the new information for all future users.

RAG is primarily a machine learning model training algorithm used to replace pre-training.

### How to use RAG:
1. Search documents.
2. Run backpropagation on the transformer weights.
3. Save the new model checkpoint.
"""

# Flawed draft 3: Abstract definition with no everyday analogy or real example
FLAWED_NO_ANALOGY_CONTENT = """# Introduction to RAG (Retrieval-Augmented Generation)

Retrieval-Augmented Generation is a software architecture for artificial intelligence systems.

### Definition
RAG consists of two components: a retrieval system and a generation system. The retrieval system searches an external database for documents matching the user's input string. The generation system is a language model that produces text based on input tokens.

### Pipeline
1. Input string is submitted by the user.
2. The retrieval component executes an information retrieval query against a document store.
3. The retrieved text documents are appended to the input string.
4. The composite text is passed to the language model.
5. The language model generates output text.

### Importance
This architecture allows systems to access data that was not present in the original dataset used during model training. It reduces errors in factual question answering tasks.

### Conclusion
RAG combines search technology with generative models to produce outputs conditioned on external data sources.
"""


def get_mock_draft(topic: str, iteration: int = 1, deliberate_flaw: str = None) -> str:
    """Return mock draft based on iteration and deliberate flaw setting."""
    if deliberate_flaw == "jargon":
        return FLAWED_JARGON_CONTENT
    elif deliberate_flaw == "hallucination":
        return FLAWED_HALLUCINATION_CONTENT
    elif deliberate_flaw == "no_analogy":
        return FLAWED_NO_ANALOGY_CONTENT
    else:
        # Default passing lesson
        return PASSING_LESSON_CONTENT


def get_mock_evaluation(topic: str, lesson_content: str, iteration: int) -> EvaluationResult:
    """Perform simulated evaluation using rubric logic."""
    stats = analyze_readability(lesson_content)
    text_lower = lesson_content.lower()

    checkpoints = []

    # Checkpoint 1: ACCURACY_AND_GROUNDED
    cp1_pass = True
    cp1_reason = "RAG is accurately explained as contextual prompt augmentation without modifying model weights."
    cp1_snippets = []
    cp1_action = "Maintain technical accuracy: emphasize external retrieval over weight retraining."
    if "neural network weights are modified" in text_lower or "retraining the artificial neural network" in text_lower or "gradient descent" in text_lower:
        cp1_pass = False
        cp1_reason = "CRITICAL FACTUAL ERROR: Lesson incorrectly claims RAG modifies neural network weights and retrains the model on the fly."
        cp1_snippets = ["The internal neural network weights of the LLM are modified directly", "RAG is primarily a machine learning model training algorithm"]
        cp1_action = "Clarify that RAG never touches internal model weights; it only inserts retrieved text into the prompt context for the LLM to read."

    checkpoints.append(CheckpointResult(
        checkpoint_id="CP1",
        name="ACCURACY_AND_GROUNDED",
        dimension="Technical Groundedness",
        passed=cp1_pass,
        score=1 if cp1_pass else 0,
        reason=cp1_reason,
        offending_snippets=cp1_snippets,
        prescriptive_action=cp1_action
    ))

    # Checkpoint 2: BEGINNER_FRIENDLY_LANGUAGE
    cp2_pass = True
    cp2_reason = f"Language is simple, accessible, and structured with short sentences (FK Grade: {stats.flesch_kincaid_grade}, Avg Sentence Length: {stats.avg_sentence_length} words)."
    cp2_snippets = []
    cp2_action = "Keep sentences short and vocabulary accessible."
    if stats.flesch_kincaid_grade > 8.5 or stats.avg_sentence_length > 20.0 or "orthogonal paradigms shift" in text_lower:
        cp2_pass = False
        cp2_reason = f"Language is far too dense for a 12th-grade non-English medium learner. FK Grade is {stats.flesch_kincaid_grade} (Target <= 7.5), Avg Sentence: {stats.avg_sentence_length} words."
        cp2_snippets = ["orthogonal paradigms shift in probabilistic autoregressive transformer architectures", "epistemic uncertainty precipitates stochastic hallucinations"]
        cp2_action = "Break long sentences down to under 16 words. Replace academic jargon with simple, conversational explanations."

    checkpoints.append(CheckpointResult(
        checkpoint_id="CP2",
        name="BEGINNER_FRIENDLY_LANGUAGE",
        dimension="Audience Accessibility",
        passed=cp2_pass,
        score=1 if cp2_pass else 0,
        reason=cp2_reason,
        offending_snippets=cp2_snippets,
        prescriptive_action=cp2_action
    ))

    # Checkpoint 3: TEACHES_BY_EXAMPLE
    cp3_pass = True
    cp3_reason = "Features a strong, relatable analogy (Open-Book vs Closed-Book Exam) and a step-by-step query walkthrough."
    cp3_snippets = []
    cp3_action = "Continue using relatable student analogies and real query walkthroughs."
    if not stats.has_relatable_analogy or "open-book" not in text_lower and "exam" not in text_lower and "library" not in text_lower:
        cp3_pass = False
        cp3_reason = "Missing a relatable real-world analogy. The lesson explains the topic in abstract theory without grounding it in familiar student experiences."
        cp3_snippets = ["RAG consists of two components: a retrieval system and a generation system."]
        cp3_action = "Introduce the classic Open-Book vs Closed-Book exam analogy right in the beginning, and walk through a real-world query step-by-step."

    checkpoints.append(CheckpointResult(
        checkpoint_id="CP3",
        name="TEACHES_BY_EXAMPLE",
        dimension="Relatable Pedagogical Anchoring",
        passed=cp3_pass,
        score=1 if cp3_pass else 0,
        reason=cp3_reason,
        offending_snippets=cp3_snippets,
        prescriptive_action=cp3_action
    ))

    # Checkpoint 4: NO_UNEXPLAINED_JARGON
    cp4_pass = True
    cp4_reason = "All technical terms (LLM, Embeddings, Prompt, Hallucination) are demystified immediately with everyday analogies."
    cp4_snippets = []
    cp4_action = "Keep explaining every term immediately upon first mention."
    if stats.unexplained_jargon_found or "bi-encoder dual-tower" in text_lower or "non-euclidean manifold" in text_lower:
        cp4_pass = False
        jargon_list = stats.unexplained_jargon_found or ["bi-encoder", "non-euclidean manifold", "cosine similarity"]
        cp4_reason = f"Detected unexplained technical jargon: {', '.join(jargon_list[:3])}. This intimidates beginner students."
        cp4_snippets = [f"Unexplained jargon instance: '{j}'" for j in jargon_list[:2]]
        cp4_action = "Never mention technical terms without an immediate 'in simple words' definition or everyday comparison (e.g. GPS coordinates for embeddings)."

    checkpoints.append(CheckpointResult(
        checkpoint_id="CP4",
        name="NO_UNEXPLAINED_JARGON",
        dimension="Cognitive Load Management",
        passed=cp4_pass,
        score=1 if cp4_pass else 0,
        reason=cp4_reason,
        offending_snippets=cp4_snippets,
        prescriptive_action=cp4_action
    ))

    # Checkpoint 5: COVERS_KEY_POINTS
    cp5_pass = True
    cp5_reason = "Covers all key points: LLM hallucination problem, acronym meaning (Retrieve, Augment, Generate), 3 steps, and career value."
    cp5_snippets = []
    cp5_action = "Maintain complete pedagogical coverage."
    has_acronym = "retrieval" in text_lower and "augmented" in text_lower and "generation" in text_lower
    has_problem = "hallucinat" in text_lower or "guessing" in text_lower or "outdated" in text_lower or "closed-book" in text_lower
    if not (has_acronym and has_problem):
        cp5_pass = False
        cp5_reason = "Missing essential foundational concepts (the hallucination problem or full acronym breakdown)."
        cp5_snippets = []
        cp5_action = "Ensure the problem (why AI lies/hallucinates) and the full meaning of R-A-G are explicitly explained."

    checkpoints.append(CheckpointResult(
        checkpoint_id="CP5",
        name="COVERS_KEY_POINTS",
        dimension="Curricular Completeness",
        passed=cp5_pass,
        score=1 if cp5_pass else 0,
        reason=cp5_reason,
        offending_snippets=cp5_snippets,
        prescriptive_action=cp5_action
    ))

    # Checkpoint 6: COHERENT_TEACHING_FLOW
    cp6_pass = True
    cp6_reason = "Pedagogical arc flows logically from hook to analogy, 3 steps, real example, and concludes with a check-for-understanding quiz."
    cp6_snippets = []
    cp6_action = "Maintain structured flow with quiz reinforcement."
    if not stats.has_check_for_understanding:
        cp6_pass = False
        cp6_reason = "Missing active learning reinforcement: No 'Check Your Understanding' mini-quiz was found."
        cp6_snippets = []
        cp6_action = "Add a 2-3 question mini-quiz at the end with immediate answers and friendly explanations."

    checkpoints.append(CheckpointResult(
        checkpoint_id="CP6",
        name="COHERENT_TEACHING_FLOW",
        dimension="Pedagogical Structure & Verification",
        passed=cp6_pass,
        score=1 if cp6_pass else 0,
        reason=cp6_reason,
        offending_snippets=cp6_snippets,
        prescriptive_action=cp6_action
    ))

    passed_count = sum(1 for cp in checkpoints if cp.passed)
    total_count = len(checkpoints)
    is_passing = (passed_count == total_count)

    critique = (
        "Lesson satisfies all 6 hard checkpoints! Exceptional clarity, grounded examples, and perfect tone for an Indian 12th-grade beginner."
        if is_passing
        else f"Lesson rejected: Failed {total_count - passed_count} of {total_count} checkpoints. Must be revised to meet strict beginner standards."
    )

    return EvaluationResult(
        iteration=iteration,
        is_passing=is_passing,
        passed_count=passed_count,
        total_count=total_count,
        checkpoints=checkpoints,
        readability=stats,
        overall_critique=critique
    )
