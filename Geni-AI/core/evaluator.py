"""
Lesson Evaluator Engine
Executes the 6-dimension hard pass/fail rubric using a hybrid two-tier architecture:
Tier 1: Deterministic algorithmic guards (Flesch-Kincaid, sentence length, regex jargon detection)
Tier 2: LLM-as-a-Judge binary evaluations with strict structured output schema.
"""

import os
import json
import re
from typing import Optional, Dict, Any, List
from config import GEMINI_API_KEY, OPENAI_API_KEY, GEMINI_MODEL, OPENAI_MODEL, DEFAULT_PROVIDER
from core.state import EvaluationResult, CheckpointResult, ReadabilityStats
from rubrics.lesson_rubric import analyze_readability, execute_deterministic_guards, RUBRIC_CHECKPOINTS
from prompts.evaluator_prompt import build_evaluator_prompt
from core.mock_engine import get_mock_evaluation


from core.inspectors import GroundednessInspector, LinguisticInspector, JargonInspector, PedagogyInspector


class EvaluatorEngine:
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or DEFAULT_PROVIDER

    def evaluate(self, topic: str, lesson_content: str, iteration: int = 1) -> EvaluationResult:
        """Run multi-inspector two-tier evaluation on a lesson draft."""
        
        # --- Tier 1: Deterministic Algorithmic Analysis ---
        readability_stats = analyze_readability(lesson_content)
        deterministic_violations = execute_deterministic_guards(lesson_content)
        violation_map = {cp_id: (reason, snippets) for cp_id, passed, reason, snippets in deterministic_violations if not passed}

        # --- Tier 2: Multi-Inspector Committee Evaluation ---
        if self.provider == "mock" or (not GEMINI_API_KEY and not OPENAI_API_KEY):
            # Run the 4 specialized inspectors
            cp1 = GroundednessInspector.inspect(lesson_content, [])
            cp2 = LinguisticInspector.inspect(lesson_content, readability_stats.model_dump())
            cp3 = PedagogyInspector.inspect_example(lesson_content)
            cp4 = JargonInspector.inspect(lesson_content)
            cp5 = PedagogyInspector.inspect_key_points(lesson_content)
            cp6 = PedagogyInspector.inspect_flow(lesson_content)
            
            checkpoints = [cp1, cp2, cp3, cp4, cp5, cp6]
            passed_count = sum(1 for cp in checkpoints if cp.passed)
            total_count = len(checkpoints)
            is_passing = (passed_count == total_count)

            critique = (
                "Lesson satisfies all 6 hard checkpoints! Exceptional clarity, grounded examples, and perfect tone for an Indian 12th-grade beginner."
                if is_passing
                else f"Lesson rejected: Failed {total_count - passed_count} of {total_count} checkpoints. Quality bar not met."
            )

            result = EvaluationResult(
                iteration=iteration,
                is_passing=is_passing,
                passed_count=passed_count,
                total_count=total_count,
                checkpoints=checkpoints,
                readability=readability_stats,
                overall_critique=critique
            )
            return self._apply_deterministic_overrides(result, readability_stats, violation_map)

        # Live LLM Evaluation
        raw_response_text = ""
        prompt = build_evaluator_prompt(
            topic=topic,
            lesson_content=lesson_content,
            deterministic_stats=readability_stats.model_dump()
        )

        if self.provider == "gemini" and GEMINI_API_KEY:
            try:
                from google import genai
                client = genai.Client(api_key=GEMINI_API_KEY)
                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt
                )
                raw_response_text = response.text
            except Exception as e:
                print(f"[Warning] Gemini evaluation failed: {e}. Falling back to mock evaluator.")
                result = get_mock_evaluation(topic=topic, lesson_content=lesson_content, iteration=iteration)
                return self._apply_deterministic_overrides(result, readability_stats, violation_map)

        elif self.provider == "openai" and OPENAI_API_KEY:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a strict, unyielding AI curriculum judge with zero tolerance for failure."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.0
                )
                raw_response_text = response.choices[0].message.content
            except Exception as e:
                print(f"[Warning] OpenAI evaluation failed: {e}. Falling back to mock evaluator.")
                result = get_mock_evaluation(topic=topic, lesson_content=lesson_content, iteration=iteration)
                return self._apply_deterministic_overrides(result, readability_stats, violation_map)

        # Parse LLM JSON
        parsed_eval = self._parse_llm_json(raw_response_text)
        if not parsed_eval:
            print("[Warning] Could not parse LLM evaluation JSON. Using deterministic evaluator fallback.")
            result = get_mock_evaluation(topic=topic, lesson_content=lesson_content, iteration=iteration)
            return self._apply_deterministic_overrides(result, readability_stats, violation_map)

        # Convert to EvaluationResult
        checkpoints = []
        for cp_data in parsed_eval.get("checkpoints", []):
            passed = bool(cp_data.get("passed", False))
            score = 1 if passed else 0
            checkpoints.append(CheckpointResult(
                checkpoint_id=cp_data.get("checkpoint_id", ""),
                name=cp_data.get("name", ""),
                dimension=cp_data.get("dimension", ""),
                passed=passed,
                score=score,
                reason=cp_data.get("reason", ""),
                offending_snippets=cp_data.get("offending_snippets", []),
                prescriptive_action=cp_data.get("prescriptive_action", "")
            ))

        passed_count = sum(1 for cp in checkpoints if cp.passed)
        total_count = len(checkpoints)
        is_passing = (passed_count == total_count)

        result = EvaluationResult(
            iteration=iteration,
            is_passing=is_passing,
            passed_count=passed_count,
            total_count=total_count,
            checkpoints=checkpoints,
            readability=readability_stats,
            overall_critique=parsed_eval.get("overall_critique", "")
        )

        return self._apply_deterministic_overrides(result, readability_stats, violation_map)

    def _apply_deterministic_overrides(
        self,
        result: EvaluationResult,
        stats: ReadabilityStats,
        violation_map: Dict[str, Any]
    ) -> EvaluationResult:
        """Enforce deterministic guardrails over LLM decisions (no false passes)."""
        modified_checkpoints = []
        for cp in result.checkpoints:
            if cp.checkpoint_id in violation_map:
                reason, snippets = violation_map[cp.checkpoint_id]
                # Hard override to fail if deterministic guard caught an overt error
                cp.passed = False
                cp.score = 0
                cp.reason = f"[Deterministic Guard Triggered]: {reason} (Original LLM note: {cp.reason})"
                if snippets:
                    cp.offending_snippets.extend(snippets)
            modified_checkpoints.append(cp)

        passed_count = sum(1 for cp in modified_checkpoints if cp.passed)
        total_count = len(modified_checkpoints)
        is_passing = (passed_count == total_count)

        result.checkpoints = modified_checkpoints
        result.passed_count = passed_count
        result.total_count = total_count
        result.is_passing = is_passing
        result.readability = stats
        return result

    def _parse_llm_json(self, raw_text: str) -> Optional[Dict[str, Any]]:
        """Extract and parse JSON safely from model response."""
        try:
            return json.loads(raw_text.strip())
        except Exception:
            pass

        # Try regex search for markdown block ```json ... ```
        match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except Exception:
                pass

        # Try finding outermost curly brackets
        start = raw_text.find('{')
        end = raw_text.rfind('}')
        if start != -1 and end != -1:
            try:
                return json.loads(raw_text[start:end+1].strip())
            except Exception:
                pass

        return None
