"""
State & Schema Definitions for Self-Evaluating RAG Lesson Content Generator
Strongly-typed Pydantic models for lessons, evaluations, and rejection logs.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class CheckpointResult(BaseModel):
    """Result of a single hard pass/fail checkpoint."""
    checkpoint_id: str
    name: str
    dimension: str
    passed: bool
    score: int = Field(description="Strict binary: 1 for Pass, 0 for Fail")
    reason: str
    offending_snippets: List[str] = Field(default_factory=list)
    prescriptive_action: str = Field(
        default="",
        description="Exact guidance for the generator on how to fix this on retry"
    )


class ReadabilityStats(BaseModel):
    """Algorithmic and cognitive readability indicators."""
    flesch_kincaid_grade: float
    avg_sentence_length: float
    total_words: int
    total_sentences: int
    coleman_liau_index: float = 0.0
    gunning_fog_index: float = 0.0
    easy_word_percentage: float = 0.0
    sentence_length_std_dev: float = 0.0
    cognitive_accessibility_score: float = 0.0
    unexplained_jargon_found: List[str] = Field(default_factory=list)
    has_relatable_analogy: bool = False
    has_check_for_understanding: bool = False


class EvaluationResult(BaseModel):
    """Full evaluation of a lesson across all rubric dimensions."""
    iteration: int
    is_passing: bool = Field(description="True ONLY if 100% of checkpoints pass")
    passed_count: int
    total_count: int
    checkpoints: List[CheckpointResult]
    readability: ReadabilityStats
    overall_critique: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class LessonDraft(BaseModel):
    """A generated lesson draft for a given topic."""
    topic: str
    iteration: int
    content: str
    deliberate_flaw: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class RejectionLogEntry(BaseModel):
    """Audit entry documenting an evaluation failure and corrective action."""
    iteration: int
    failed_checkpoints: List[str]
    root_cause_analysis: str
    offending_snippets: List[str]
    targeted_feedback: str
    action_taken_on_retry: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class PipelineRunResult(BaseModel):
    """Complete summary of an agentic run."""
    run_id: str
    topic: str
    provider: str
    is_approved: bool
    total_iterations: int
    final_lesson: str
    evaluations: List[EvaluationResult]
    rejection_log: List[RejectionLogEntry]
    evolved_rules_applied: List[str] = Field(default_factory=list)
    newly_evolved_rules: List[str] = Field(default_factory=list)
    retrieved_context_chunks: List[Dict[str, Any]] = Field(default_factory=list)
    iteration_diffs: List[Dict[str, Any]] = Field(default_factory=list)
    telemetry: Dict[str, Any] = Field(default_factory=dict)
    target_persona: str = "12th-Grade Graduate from India (Non-English Medium Background)"
    started_at: str
    completed_at: str
