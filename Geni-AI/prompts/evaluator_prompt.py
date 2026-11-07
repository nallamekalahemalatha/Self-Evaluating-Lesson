"""
Evaluator Prompt Templates
Strict, zero-partial-credit judge prompt that checks all 6 rubric dimensions.
"""

import json
from typing import Dict, Any


def build_evaluator_prompt(topic: str, lesson_content: str, deterministic_stats: Dict[str, Any]) -> str:
    """Build the evaluation prompt with strict schema enforcement."""

    stats_summary = f"""
- Flesch-Kincaid Grade Level: {deterministic_stats.get('flesch_kincaid_grade', 'N/A')} (Target <= 7.5)
- Average Sentence Length: {deterministic_stats.get('avg_sentence_length', 'N/A')} words (Target <= 18 words)
- Total Word Count: {deterministic_stats.get('total_words', 'N/A')} words
- Potentially Unexplained Jargon Detected by Scanner: {deterministic_stats.get('unexplained_jargon_found', [])}
- Relatable Analogy Detected: {deterministic_stats.get('has_relatable_analogy', False)}
- Check for Understanding Quiz Detected: {deterministic_stats.get('has_check_for_understanding', False)}
"""

    prompt = f"""You are an unyielding, rigorous Lead AI Curriculum Evaluator. Your role is NOT to be generous — it is to decide whether this lesson clears strict production quality standards before a vulnerable beginner student ever sees it.

The target audience is an Indian 12th-grade graduate from a non-English-medium school who is working to enter the AI field. If the lesson uses dense jargon, long academic sentences, or confusing explanations, this student will get discouraged and give up.

### The Topic:
"{topic}"

### Pre-computed Algorithmic Scanner Diagnostics:
{stats_summary}

### The 6 Hard Pass/Fail Checkpoints (ZERO Partial Credit):
1. **CP1: ACCURACY_AND_GROUNDED**
   - PASS criteria: The lesson accurately explains RAG as fetching external context and feeding it to the AI prompt without altering internal model weights.
   - FAIL criteria: It claims RAG modifies neural network weights, retrains the model, or misrepresents AI fundamentals.

2. **CP2: BEGINNER_FRIENDLY_LANGUAGE**
   - PASS criteria: Language is plain, welcoming, and easy to follow. Sentences are short and crisp. Uses simple vocabulary accessible to a 12th-grade non-English medium learner.
   - FAIL criteria: Heavy academic vocabulary, overly complex sentence structures, or passive voice overload.

3. **CP3: TEACHES_BY_EXAMPLE**
   - PASS criteria: Features at least one relatable, vivid real-world analogy (e.g. Open-Book vs Closed-Book Exam, student visiting school library) AND walks through a concrete step-by-step query example.
   - FAIL criteria: Purely theoretical or abstract definitions with no relatable comparison or concrete walkthrough.

4. **CP4: NO_UNEXPLAINED_JARGON**
   - PASS criteria: Every technical term (like Embeddings, Vectors, LLM, Hallucination, Retrieval, Prompt) is immediately demystified in simple words using an analogy before continuing.
   - FAIL criteria: Dropping technical buzzwords without immediate plain-English translation or explanation.

5. **CP5: COVERS_KEY_POINTS**
   - PASS criteria: Thoroughly explains: (a) Why AI makes up false answers / lacks updated info, (b) What RAG stands for word-by-word, (c) The 3-step mechanics (Retrieve -> Augment -> Generate), and (d) Why RAG is valuable for industry jobs.
   - FAIL criteria: Missing any of these core pedagogical pillars.

6. **CP6: COHERENT_TEACHING_FLOW**
   - PASS criteria: Clear pedagogical sequence: Hook/Problem -> Intuitive Analogy -> 3-Step Process -> Real-World Example -> Summary -> 'Check Your Understanding' mini-quiz.
   - FAIL criteria: Disjointed flow, abrupt topic leaps, or lack of a self-assessment quiz.

### Lesson Draft Under Evaluation:
\"\"\"
{lesson_content}
\"\"\"

### Output Format Requirement:
You MUST respond with a single, valid JSON object strictly adhering to this structure:
{{
  "is_passing": boolean, // true ONLY if all 6 checkpoints pass. If even one fails, this MUST be false!
  "checkpoints": [
    {{
      "checkpoint_id": "CP1",
      "name": "ACCURACY_AND_GROUNDED",
      "dimension": "Technical Groundedness",
      "passed": boolean,
      "score": 1 or 0,
      "reason": "Clear explanation of why it passed or failed",
      "offending_snippets": ["exact snippet from draft causing failure, if any"],
      "prescriptive_action": "Specific instructions on how to fix this"
    }},
    {{
      "checkpoint_id": "CP2",
      "name": "BEGINNER_FRIENDLY_LANGUAGE",
      "dimension": "Audience Accessibility",
      "passed": boolean,
      "score": 1 or 0,
      "reason": "...",
      "offending_snippets": [],
      "prescriptive_action": "..."
    }},
    {{
      "checkpoint_id": "CP3",
      "name": "TEACHES_BY_EXAMPLE",
      "dimension": "Relatable Pedagogical Anchoring",
      "passed": boolean,
      "score": 1 or 0,
      "reason": "...",
      "offending_snippets": [],
      "prescriptive_action": "..."
    }},
    {{
      "checkpoint_id": "CP4",
      "name": "NO_UNEXPLAINED_JARGON",
      "dimension": "Cognitive Load Management",
      "passed": boolean,
      "score": 1 or 0,
      "reason": "...",
      "offending_snippets": [],
      "prescriptive_action": "..."
    }},
    {{
      "checkpoint_id": "CP5",
      "name": "COVERS_KEY_POINTS",
      "dimension": "Curricular Completeness",
      "passed": boolean,
      "score": 1 or 0,
      "reason": "...",
      "offending_snippets": [],
      "prescriptive_action": "..."
    }},
    {{
      "checkpoint_id": "CP6",
      "name": "COHERENT_TEACHING_FLOW",
      "dimension": "Pedagogical Structure & Verification",
      "passed": boolean,
      "score": 1 or 0,
      "reason": "...",
      "offending_snippets": [],
      "prescriptive_action": "..."
    }}
  ],
  "overall_critique": "A brief 2-3 sentence executive summary of the evaluation verdict."
}}
Do NOT output any markdown backticks around the JSON if possible, or use standard ```json. Return ONLY valid JSON.
"""
    return prompt
