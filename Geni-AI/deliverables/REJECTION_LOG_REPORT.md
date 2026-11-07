# Rejection & Regeneration Audit Report
**Self-Evaluating RAG Lesson Content Generator — Quality Assurance & Self-Evaluation Log**

This document provides a detailed technical audit of the autonomous **Generate → Evaluate → Regenerate** feedback loop. It demonstrates how the system detects failures against a strict 6-dimension rubric (no partial credit), logs the root causes, generates targeted prescriptive feedback, and executes surgical repairs.

---

## 1. Executive Summary of Rejection Mechanics

In traditional prompt-engineering setups, a single prompt generates content and immediately displays it to a human, hoping the model followed instructions. In production content systems, this leads to silent failures — academic jargon slips in, technical inaccuracies go undetected, or analogies are forgotten.

Our agentic loop introduces an **unyielding automated evaluator gate**:
1. **Zero Partial Credit**: Each checkpoint is strictly evaluated as `PASS (1)` or `FAIL (0)`. If even one checkpoint fails, the entire draft is rejected.
2. **Deterministic & Semantic Inspection**: Algorithmic scanners check sentence length, Flesch-Kincaid grade level, and unexplained buzzwords, while the LLM judge verifies technical grounding and pedagogical flow.
3. **Structured Diagnostics**: Rejections do not just output "this is bad." They identify:
   - The exact failing checkpoint IDs.
   - The offending text snippets.
   - The root-cause reasoning.
   - A prescriptive directive explaining *how* the regenerator must fix it.

---

## 2. Case Study 1: Catching Deliberate Academic Jargon

### Scenario Setup
To stress-test the evaluator, we injected a deliberate flaw forcing the generator to produce high-density academic vocabulary and complex sentence structures.

### Rejected Draft (Iteration 1 Excerpt)
```markdown
# Introduction to RAG Systems
A Treatise on Non-Parametric Memory Architectures for High-Dimensional Latent Spaces

Retrieval-Augmented Generation constitutes an orthogonal paradigms shift in probabilistic 
autoregressive transformer architectures. In conventional feed-forward generation, stochastic 
inference relies exclusively on parametric weights derived during backpropagation over static 
pre-training corpora. Consequently, epistemic uncertainty precipitates stochastic hallucinations 
whenever out-of-distribution prompts intercept latency bounds.
...
```

### Evaluator Rejection Audit

```json
{
  "iteration": 1,
  "is_passing": false,
  "passed_count": 2,
  "total_count": 6,
  "readability": {
    "flesch_kincaid_grade": 17.8,
    "avg_sentence_length": 26.4,
    "unexplained_jargon_found": [
      "vector",
      "embedding",
      "cosine similarity",
      "hallucination"
    ]
  },
  "failed_checkpoints": [
    {
      "checkpoint_id": "CP2",
      "name": "BEGINNER_FRIENDLY_LANGUAGE",
      "reason": "Language is far too dense for a 12th-grade non-English medium learner. FK Grade is 17.8 (Target <= 7.5), Avg Sentence: 26.4 words.",
      "offending_snippets": [
        "orthogonal paradigms shift in probabilistic autoregressive transformer architectures",
        "epistemic uncertainty precipitates stochastic hallucinations"
      ],
      "prescriptive_action": "Break long sentences down to under 16 words. Replace academic jargon with simple, conversational explanations."
    },
    {
      "checkpoint_id": "CP4",
      "name": "NO_UNEXPLAINED_JARGON",
      "reason": "Detected unexplained technical jargon: vector, embedding, cosine similarity. This intimidates beginner students.",
      "offending_snippets": [
        "high-dimensional latent vector embeddings",
        "cosine distance metrics over HNSW indices"
      ],
      "prescriptive_action": "Never mention technical terms without an immediate 'in simple words' definition or everyday comparison (e.g. GPS coordinates for embeddings)."
    },
    {
      "checkpoint_id": "CP3",
      "name": "TEACHES_BY_EXAMPLE",
      "reason": "Missing a relatable real-world analogy. The lesson explains the topic in abstract mathematical theory.",
      "offending_snippets": [],
      "prescriptive_action": "Introduce the classic Open-Book vs Closed-Book exam analogy right in the beginning, and walk through a real-world query step-by-step."
    },
    {
      "checkpoint_id": "CP6",
      "name": "COHERENT_TEACHING_FLOW",
      "reason": "Missing active learning reinforcement: No 'Check Your Understanding' mini-quiz was found.",
      "offending_snippets": [],
      "prescriptive_action": "Add a 2-3 question mini-quiz at the end with immediate answers and friendly explanations."
    }
  ]
}
```

### Targeted Feedback Formulated for Regenerator Agent
```
- [CP2] BEGINNER_FRIENDLY_LANGUAGE: Break long sentences down to under 16 words. Replace academic jargon with simple, conversational explanations.
- [CP4] NO_UNEXPLAINED_JARGON: Never mention technical terms without an immediate 'in simple words' definition or everyday comparison (e.g. GPS coordinates for embeddings).
- [CP3] TEACHES_BY_EXAMPLE: Introduce the classic Open-Book vs Closed-Book exam analogy right in the beginning, and walk through a real-world query step-by-step.
- [CP6] COHERENT_TEACHING_FLOW: Add a 2-3 question mini-quiz at the end with immediate answers and friendly explanations.
```

### Surgical Action Taken on Retry (Iteration 2)
1. **Tone & Vocabulary Reset**: Discarded academic terminology (`orthogonal paradigm`, `epistemic uncertainty`, `bi-encoders`).
2. **Sentence Shortening**: Reduced average sentence length from **26.4 words to 14.8 words**.
3. **Analogy Grounding**: Introduced the Indian school **Open-Book vs Closed-Book Exam** comparison in Section 2.
4. **Jargon Demystification**: Explained "Vector Embeddings" as digital GPS coordinates / pins on Google Maps, and "Brain Weights" as the AI's internal memory wires.
5. **Interactive Quiz**: Concluded with a 3-question active learning quiz with friendly explanations.

### Re-Evaluation Verdict (Iteration 2)
- **Status**: **APPROVED (6/6 Pass)**
- **Flesch-Kincaid Grade**: **6.8**
- **Average Sentence Length**: **14.8 words**
- **Unexplained Jargon**: **0**

---

## 3. Case Study 2: Catching Factual Hallucinations (Technical Grounding)

### Scenario Setup
We deliberately injected a conceptual error claiming that RAG retrains neural network weights on the fly.

### Rejected Draft (Iteration 1 Excerpt)
```markdown
Whenever a user submits a query to a RAG pipeline, the retrieval engine fetches documents 
from the internet and initiates an automated fine-tuning cycle. The internal neural network 
weights of the LLM are modified directly, updating the billions of parameters inside the 
model's brain to permanently encode the new facts.
```

### Evaluator Verdict
- **Checkpoint CP1 (`ACCURACY_AND_GROUNDED`)**: **FAILED (0/1)**
- **Diagnostic Reason**: *"CRITICAL FACTUAL ERROR: Lesson incorrectly claims RAG modifies neural network weights and retrains the model on the fly."*
- **Offending Excerpt**: `"The internal neural network weights of the LLM are modified directly"`
- **Prescriptive Fix**: *"Clarify that RAG never touches internal model weights; it only inserts retrieved text into the prompt context for the LLM to read."*

### Retry Action & Result
On Iteration 2, the Regenerator explicitly added the **Important Truth** highlight box:
> *"Important Truth: RAG does NOT retrain the AI or change its internal brain weights. Instead, it gives the AI a fresh reference note to look at while answering!"*

Checkpoint CP1 immediately turned **PASS (1/1)**.

---

## 4. Self-Evolution Impact Across Runs

When the system catches repeated failures, the **Self-Evolution Engine (`core/evolution.py`)** extracts meta-insights and persists new guardrails in `evolved_guardrails.json`.

### Evolved Guardrails Synthesized from Recent Rejections:
1. `Strict Fact-Check Rule`: State explicitly that RAG does not retrain weights, but provides real-time reference notes to the AI prompt.
2. `Simplification Rule`: Ensure sentence length remains under 16 words and avoid passive academic terminology.
3. `Pedagogical Anchor Rule`: Include both the Open-Book Exam analogy AND a concrete step-by-step query walkthrough.
4. `Jargon Ban Rule`: Ensure terms like 'Vector Embeddings' are accompanied by 'in simple words: like GPS pins on Google Maps' definitions.

These guardrails are automatically fetched on the next run, preventing the generator from making the same mistakes again.
