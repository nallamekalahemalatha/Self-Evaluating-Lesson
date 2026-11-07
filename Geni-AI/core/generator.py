"""
Lesson Content Generator Agent
Generates lesson drafts using LLMs (Gemini/OpenAI) or Mock Simulation.
"""

import os
from typing import Optional, List
from config import GEMINI_API_KEY, OPENAI_API_KEY, GEMINI_MODEL, OPENAI_MODEL, DEFAULT_PROVIDER
from prompts.generator_prompt import build_generator_prompt
from core.mock_engine import get_mock_draft
from core.state import LessonDraft


class GeneratorAgent:
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or DEFAULT_PROVIDER

    def generate(
        self,
        topic: str,
        iteration: int = 1,
        evolved_guardrails: Optional[List[str]] = None,
        deliberate_flaw: Optional[str] = None
    ) -> LessonDraft:
        """Generate a lesson draft for the given topic and persona."""
        
        prompt = build_generator_prompt(
            topic=topic,
            evolved_guardrails=evolved_guardrails,
            deliberate_flaw=deliberate_flaw
        )

        content = ""
        # 1. Mock execution
        if self.provider == "mock" or (not GEMINI_API_KEY and not OPENAI_API_KEY):
            content = get_mock_draft(topic=topic, iteration=iteration, deliberate_flaw=deliberate_flaw)
        
        # 2. Gemini execution
        elif self.provider == "gemini" and GEMINI_API_KEY:
            try:
                from google import genai
                client = genai.Client(api_key=GEMINI_API_KEY)
                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt
                )
                content = response.text
            except Exception as e:
                # Graceful fallback to mock on network/auth issue
                print(f"[Warning] Gemini generation failed: {e}. Falling back to mock engine.")
                content = get_mock_draft(topic=topic, iteration=iteration, deliberate_flaw=deliberate_flaw)

        # 3. OpenAI execution
        elif self.provider == "openai" and OPENAI_API_KEY:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a master GenAI educator building lessons for Indian high-school graduates."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                content = response.choices[0].message.content
            except Exception as e:
                print(f"[Warning] OpenAI generation failed: {e}. Falling back to mock engine.")
                content = get_mock_draft(topic=topic, iteration=iteration, deliberate_flaw=deliberate_flaw)
        
        else:
            content = get_mock_draft(topic=topic, iteration=iteration, deliberate_flaw=deliberate_flaw)

        return LessonDraft(
            topic=topic,
            iteration=iteration,
            content=content,
            deliberate_flaw=deliberate_flaw
        )
