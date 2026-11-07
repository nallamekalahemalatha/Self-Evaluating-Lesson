"""
Lesson Rubric & Algorithmic Guardrails
Defines the 6 hard pass/fail checkpoints (no partial credit) and deterministic analyzers.
"""

import re
import math
from typing import List, Dict, Tuple, Any
from core.state import CheckpointResult, ReadabilityStats


RUBRIC_CHECKPOINTS = [
    {
        "id": "CP1",
        "name": "ACCURACY_AND_GROUNDED",
        "dimension": "Technical Groundedness",
        "description": "Technically correct description of RAG. External facts are retrieved and added to prompt context without altering model weights. No confusion with fine-tuning or training.",
        "failure_criterion": "States or implies that RAG trains/retrains the model, modifies internal neural network weights, or hallucinates architectural facts."
    },
    {
        "id": "CP2",
        "name": "BEGINNER_FRIENDLY_LANGUAGE",
        "dimension": "Audience Accessibility",
        "description": "Accessible to an Indian 12th-grade graduate from a non-English medium background. Average sentence length <= 18 words, Flesch-Kincaid Grade Level <= 7.5.",
        "failure_criterion": "Dense academic sentence structures, passive voice overuse, vocabulary beyond 12th-grade Indian non-native English comprehension."
    },
    {
        "id": "CP3",
        "name": "TEACHES_BY_EXAMPLE",
        "dimension": "Relatable Pedagogical Anchoring",
        "description": "Grounds the topic in at least one concrete everyday analogy (e.g., open-book vs closed-book exam, library reference assistant) and walks through a real query step-by-step.",
        "failure_criterion": "Purely theoretical or abstract descriptions without concrete everyday analogies or query walkthrough."
    },
    {
        "id": "CP4",
        "name": "NO_UNEXPLAINED_JARGON",
        "dimension": "Cognitive Load Management",
        "description": "Every technical term (Vector, Embedding, Hallucination, Retrieval, Token, LLM) must be defined in plain words before or immediately upon introduction.",
        "failure_criterion": "Using technical buzzwords or acronyms without an immediate plain-English explanation or analogy."
    },
    {
        "id": "CP5",
        "name": "COVERS_KEY_POINTS",
        "dimension": "Curricular Completeness",
        "description": "Must cover: (1) The Problem (LLMs hallucinate and lack fresh knowledge), (2) What RAG stands for, (3) The 3-Step Process (Retrieve -> Augment -> Generate), (4) Why it matters.",
        "failure_criterion": "Omitting any of the core pillars: the hallucination problem, the full acronym breakdown, the 3 steps, or real-world importance."
    },
    {
        "id": "CP6",
        "name": "COHERENT_TEACHING_FLOW",
        "dimension": "Pedagogical Structure & Verification",
        "description": "Logical progression: Hook/Problem -> The Intuitive Solution -> Step-by-Step Breakdown -> Concrete Walkthrough -> Summary -> 'Check Your Understanding' mini-quiz.",
        "failure_criterion": "Disjointed structure, jumping between technical details without logical transitions, or missing comprehension check."
    }
]

# Sensitive Jargon Registry that must be explained
TECHNICAL_JARGON = [
    "vector",
    "embedding",
    "embeddings",
    "hallucination",
    "hallucinate",
    "cosine similarity",
    "context window",
    "retrieval",
    "semantic search",
    "tokens",
    "parameters",
    "fine-tuning",
    "weights"
]

EXPLANATION_MARKERS = [
    "like a",
    "think of",
    "means",
    "in simple words",
    "simply put",
    "just like",
    "for example",
    "imagine",
    "which is",
    "analogous to",
    "similar to"
]


def count_syllables(word: str) -> int:
    """Estimate syllables in an English word."""
    word = word.lower().strip(".,!?:;\"'()[]{}")
    if not word:
        return 0
    if len(word) <= 3:
        return 1
    word = re.sub(r'(?:[^laeiouy]|ed|es|e)$', '', word)
    word = re.sub(r'^y', '', word)
    matches = re.findall(r'[aeiouy]{1,2}', word)
    return max(1, len(matches))


def analyze_readability(text: str) -> ReadabilityStats:
    """Calculate deterministic readability metrics and scan for unexplained jargon."""
    clean_text = re.sub(r'#+\s*', '', text)  # remove markdown headers
    clean_text = re.sub(r'[*_`]', '', clean_text)  # remove markdown styling

    # Sentences split
    raw_sentences = [s.strip() for s in re.split(r'[.!?]+', clean_text) if s.strip()]
    total_sentences = max(1, len(raw_sentences))

    # Words split
    words = [w for w in re.findall(r'\b[a-zA-Z]+\b', clean_text)]
    total_words = max(1, len(words))

    # Syllables
    total_syllables = sum(count_syllables(w) for w in words)

    # Flesch-Kincaid Grade Level: 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
    words_per_sentence = total_words / total_sentences
    syllables_per_word = total_syllables / total_words
    fk_grade = 0.39 * words_per_sentence + 11.8 * syllables_per_word - 15.59
    fk_grade = round(max(0.0, fk_grade), 2)
    avg_sentence_len = round(words_per_sentence, 2)

    text_lower = text.lower()
    # Remove heading lines before scanning body prose for jargon
    body_lines = [line for line in text.splitlines() if not line.strip().startswith('#')]
    body_text_lower = " ".join(body_lines).lower()

    # Scan for unexplained jargon
    unexplained = []
    for jargon in TECHNICAL_JARGON:
        pattern = rf'\b{re.escape(jargon)}\b'
        matches = list(re.finditer(pattern, body_text_lower))
        if matches:
            # Check if this term is explicitly explained anywhere in the document
            # Either via a definition item (- **Term... or Term: ... in simple words)
            # or within proximity of any of its occurrences
            is_explained = False
            
            # Check for dedicated explanation block or glossary
            glossary_pattern = rf'\b{re.escape(jargon)}\b[^\n.!?]*?(?:in simple words|think of|means|like a|synonym|searching|fetching|gps pin|library|memory)'
            if re.search(glossary_pattern, body_text_lower):
                is_explained = True
            else:
                # Proximity check on the first occurrence
                first_idx = matches[0].start()
                start_window = max(0, first_idx - 150)
                end_window = min(len(body_text_lower), first_idx + 220)
                surrounding = body_text_lower[start_window:end_window]
                if any(marker in surrounding for marker in EXPLANATION_MARKERS):
                    is_explained = True

            if not is_explained:
                unexplained.append(jargon)

    # Calculate comprehensive metrics
    from rubrics.advanced_metrics import compute_comprehensive_metrics
    adv_metrics = compute_comprehensive_metrics(text)

    # Check for relatable analogy anchors
    analogy_keywords = [
        "exam", "library", "book", "librarian", "student", "teacher", 
        "open book", "closed book", "guide", "memory", "chit", "notes"
    ]
    has_analogy = any(ak in text_lower for ak in analogy_keywords)

    # Check for check of understanding quiz
    has_quiz = any(qk in text_lower for qk in [
        "check your understanding", 
        "quiz", 
        "quick question", 
        "test your understanding",
        "question 1"
    ])

    return ReadabilityStats(
        flesch_kincaid_grade=adv_metrics["flesch_kincaid_grade"],
        avg_sentence_length=adv_metrics["avg_sentence_length"],
        total_words=adv_metrics["total_words"],
        total_sentences=adv_metrics["total_sentences"],
        coleman_liau_index=adv_metrics["coleman_liau_index"],
        gunning_fog_index=adv_metrics["gunning_fog_index"],
        easy_word_percentage=adv_metrics["easy_word_percentage"],
        sentence_length_std_dev=adv_metrics["sentence_length_std_dev"],
        cognitive_accessibility_score=adv_metrics["cognitive_accessibility_score"],
        unexplained_jargon_found=unexplained,
        has_relatable_analogy=has_analogy,
        has_check_for_understanding=has_quiz
    )


def execute_deterministic_guards(text: str) -> List[Tuple[str, bool, str, List[str]]]:
    """
    Run fast rule-based guards to spot clear violations before or alongside LLM analysis.
    Returns: list of (checkpoint_id, passed, reason, offending_snippets)
    """
    stats = analyze_readability(text)
    guards_results = []

    # Checkpoint 2: BEGINNER_FRIENDLY_LANGUAGE (Deterministic component)
    cp2_pass = True
    cp2_reasons = []
    cp2_snippets = []
    if stats.flesch_kincaid_grade > 9.0:
        cp2_pass = False
        cp2_reasons.append(f"Flesch-Kincaid Grade Level is {stats.flesch_kincaid_grade} (Target <= 7.5). Sentences are too complex for non-English medium graduates.")
    if stats.avg_sentence_length > 22.0:
        cp2_pass = False
        cp2_reasons.append(f"Average sentence length is {stats.avg_sentence_length} words (Target <= 18 words). Break long sentences into short, crisp statements.")
    
    if not cp2_pass:
        guards_results.append((
            "CP2",
            False,
            "; ".join(cp2_reasons),
            cp2_snippets
        ))

    # Checkpoint 4: NO_UNEXPLAINED_JARGON (Deterministic component)
    if stats.unexplained_jargon_found:
        guards_results.append((
            "CP4",
            False,
            f"Detected technical terms introduced without an immediate plain-language analogy: {', '.join(stats.unexplained_jargon_found[:4])}.",
            [f"Term without anchor: '{term}'" for term in stats.unexplained_jargon_found[:3]]
        ))

    # Checkpoint 3: TEACHES_BY_EXAMPLE (Deterministic component)
    if not stats.has_relatable_analogy:
        guards_results.append((
            "CP3",
            False,
            "Lesson lacks a familiar real-world analogy (e.g., Open-Book vs Closed-Book Exam or College Library reference desk).",
            []
        ))

    # Checkpoint 6: COHERENT_TEACHING_FLOW (Quiz check)
    if not stats.has_check_for_understanding:
        guards_results.append((
            "CP6",
            False,
            "Lesson is missing a 'Check Your Understanding' mini-quiz section to test the learner's comprehension.",
            []
        ))

    return guards_results
