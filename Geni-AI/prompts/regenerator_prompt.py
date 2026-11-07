"""
Regenerator Prompt Templates
Synthesizes evaluator diagnostic feedback to direct surgical revision.
"""

from typing import List, Dict, Any


def build_regenerator_prompt(
    topic: str,
    previous_draft: str,
    failed_checkpoints: List[Dict[str, Any]],
    overall_critique: str
) -> str:
    """Build the regeneration prompt focusing on repairing specific failed checkpoints."""

    feedback_blocks = []
    for cp in failed_checkpoints:
        snippets_text = ""
        if cp.get("offending_snippets"):
            snippets_text = "\n    * Offending Snippets:\n" + "\n".join(f'      - "{s}"' for s in cp["offending_snippets"])
        
        feedback_blocks.append(
            f"- **Checkpoint Failed: {cp.get('name')} ({cp.get('checkpoint_id')})**\n"
            f"  * Root Cause: {cp.get('reason')}\n"
            f"  * Prescriptive Fix Required: {cp.get('prescriptive_action')}"
            f"{snippets_text}"
        )

    all_feedback = "\n".join(feedback_blocks)

    prompt = f"""You are an expert AI curriculum repair engineer. The previous lesson draft for "{topic}" was rejected by our strict quality evaluator.

Your task is to REGENERATE and REFINE the lesson so that it passes all 6 quality checkpoints with zero defects.

### Target Learner Persona:
An Indian 12th-grade graduate from a non-English medium background who wants to enter the AI career field. They need clear, short sentences, vivid analogies (like Open-Book vs Closed-Book exams), zero unexplained jargon, and an encouraging tone.

### Evaluator's Overall Critique:
{overall_critique}

### Hard Failures to Fix (Zero Tolerance):
{all_feedback}

### Regeneration Directives:
1. **Surgical Precision**: Fix all the specific points flagged above.
   - If technical terms were unexplained, demystify them immediately using everyday analogies.
   - If sentences were too long or academic, simplify vocabulary and break long sentences into bite-sized thoughts.
   - If the exam/library analogy was missing or weak, make it central and memorable.
   - If technical accuracy was breached, correct the factual explanation of RAG (RAG fetches external text into the prompt context; it NEVER retrains model weights).
   - If the comprehension quiz was missing or inadequate, provide 2-3 engaging questions with friendly explanations.
2. **Preserve What Worked**: Retain the clear explanations, positive tone, and logical sections that were already strong in the previous draft.
3. **Format**: Deliver a complete, standalone, production-ready lesson formatted in clean GitHub-Flavored Markdown.

### Previous Rejected Draft:
\"\"\"
{previous_draft}
\"\"\"

Now, output the revised, fully repaired lesson.
"""
    return prompt
