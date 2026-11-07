"""
Generator Prompt Templates
Crafted specifically for an Indian 12th-grade graduate from a non-English-medium background.
"""

from typing import List, Optional
from config import TARGET_PERSONA


def build_generator_prompt(topic: str, evolved_guardrails: Optional[List[str]] = None, deliberate_flaw: Optional[str] = None) -> str:
    """Build the system & user prompt for lesson generation."""

    guardrails_text = ""
    if evolved_guardrails:
        guardrails_text = "\n### Learned Guardrails from Past Runs (Pay strict attention):\n" + "\n".join(f"- {g}" for g in evolved_guardrails)

    flaw_instruction = ""
    if deliberate_flaw == "jargon":
        flaw_instruction = (
            "\n[DEMONSTRATION INJECTION - DELIBERATE FLAW ACTIVATED]:\n"
            "Intentionally inject dense, unexplained academic terms into the lesson (e.g., use 'high-dimensional latent vector embeddings', "
            "'cosine distance metrics', and 'non-parametric memory' without explaining them or using any simple analogies). "
            "Write long, complex sentences with academic phrasing. This is for testing the evaluator's ability to catch flaws.\n"
        )
    elif deliberate_flaw == "hallucination":
        flaw_instruction = (
            "\n[DEMONSTRATION INJECTION - DELIBERATE FLAW ACTIVATED]:\n"
            "Intentionally include a major technical factual error: explicitly claim that RAG updates the internal neural weights "
            "of the large language model every time a query is executed, and that RAG is a method of model retraining/fine-tuning. "
            "This is for testing the evaluator's technical grounding checkpoint.\n"
        )
    elif deliberate_flaw == "no_analogy":
        flaw_instruction = (
            "\n[DEMONSTRATION INJECTION - DELIBERATE FLAW ACTIVATED]:\n"
            "Do NOT use any real-world analogies (no exam analogies, no library analogies, no real-life comparisons). "
            "Present only abstract definitions and technical mechanics with zero everyday examples. "
            "This is for testing the evaluator's 'Teaches by Example' checkpoint.\n"
        )

    prompt = f"""You are an elite, empathetic GenAI Educator creating learning material for an Indian 12th-grade graduate who completed schooling in a regional, non-English-medium language (such as Hindi, Telugu, Tamil, Marathi, or Bengali medium).

### Learner Persona:
- **Background**: Completed 12th standard. Highly ambitious and eager to learn GenAI to build a career in technology.
- **English Comfort**: Understands simple conversational English, but feels nervous and overwhelmed when facing dense academic books, long nested sentences, or unexplained technical buzzwords.
- **Learning Style**: Learns best through vivid, everyday real-world situations (school exams, library visits, train reservation charts, cricket scorecards) and step-by-step query examples.

### Pedagogical Core Requirements for "{topic}":
1. **The Hook & Everyday Dilemma**:
   - Begin with the core limitation of standard AI: AI only knows what it learned in school (its training data). It cannot know today's train schedule or private office records! When asked something it does not know, it sometimes makes up convincing lies (called "hallucination").
2. **The Breakthrough Analogy (Open-Book vs Closed-Book Exam)**:
   - Use the classic, relatable analogy:
     - **Standard AI** is like a student writing a **Closed-Book Exam** solely from memory. If they forget or never studied a new topic, they might guess.
     - **RAG** is like an **Open-Book Exam**! The student is allowed to open a textbook, look up the exact verified page, and write the answer based on real facts.
3. **The 3 Core Steps of RAG (Break down the acronym clearly)**:
   - **R = Retrieval (Search)**: Finding the relevant fact or document.
   - **A = Augmented (Added/Attached)**: Pasting that fact into the prompt note.
   - **G = Generation (Writing the Answer)**: The AI reads the fact and generates the final reply in clear English.
4. **Concrete Step-by-Step Query Walkthrough**:
   - Walk through an actual question (e.g., "What are the new admission rules for XYZ College 2026?"). Show what happens at Step 1, Step 2, and Step 3.
5. **Why This Matters for Their AI Career**:
   - Why companies hire engineers to build RAG systems (accuracy, real-time facts, preventing false information, protecting private business documents).
6. **Language & Formatting Rules**:
   - Keep sentences short (under 18 words on average).
   - If you ever introduce a technical word like 'Vector', 'Embedding', 'LLM', or 'Prompt', IMMEDIATELY explain what it means in plain words using a simple analogy.
   - Warm, encouraging, mentorship tone.
7. **Check Your Understanding**:
   - End with 2-3 interactive multiple-choice or reflection questions with immediate, friendly explanations so the learner can celebrate getting them right!
{guardrails_text}
{flaw_instruction}

Now, write the complete, standalone beginner lesson for "{topic}". Ensure formatting is beautiful GitHub-flavored Markdown with clear headings and bullet points.
"""
    return prompt
