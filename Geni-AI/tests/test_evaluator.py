"""
Tests for Lesson Evaluator & Hard Checkpoint Rubrics
"""

import pytest
from core.evaluator import EvaluatorEngine
from core.mock_engine import (
    PASSING_LESSON_CONTENT,
    FLAWED_JARGON_CONTENT,
    FLAWED_HALLUCINATION_CONTENT,
    FLAWED_NO_ANALOGY_CONTENT
)
from rubrics.lesson_rubric import analyze_readability


def test_passing_lesson_clears_all_checkpoints():
    evaluator = EvaluatorEngine(provider="mock")
    result = evaluator.evaluate(
        topic="Introduction to RAG",
        lesson_content=PASSING_LESSON_CONTENT,
        iteration=1
    )
    assert result.is_passing is True
    assert result.passed_count == 6
    assert result.total_count == 6
    for cp in result.checkpoints:
        assert cp.passed is True
        assert cp.score == 1


def test_flawed_jargon_triggers_rejection():
    evaluator = EvaluatorEngine(provider="mock")
    result = evaluator.evaluate(
        topic="Introduction to RAG",
        lesson_content=FLAWED_JARGON_CONTENT,
        iteration=1
    )
    assert result.is_passing is False
    # Check that audience accessibility and jargon checkpoints fail
    failed_ids = [cp.checkpoint_id for cp in result.checkpoints if not cp.passed]
    assert "CP2" in failed_ids or "CP4" in failed_ids


def test_flawed_hallucination_triggers_accuracy_failure():
    evaluator = EvaluatorEngine(provider="mock")
    result = evaluator.evaluate(
        topic="Introduction to RAG",
        lesson_content=FLAWED_HALLUCINATION_CONTENT,
        iteration=1
    )
    assert result.is_passing is False
    failed_ids = [cp.checkpoint_id for cp in result.checkpoints if not cp.passed]
    assert "CP1" in failed_ids


def test_flawed_no_analogy_triggers_example_failure():
    evaluator = EvaluatorEngine(provider="mock")
    result = evaluator.evaluate(
        topic="Introduction to RAG",
        lesson_content=FLAWED_NO_ANALOGY_CONTENT,
        iteration=1
    )
    assert result.is_passing is False
    failed_ids = [cp.checkpoint_id for cp in result.checkpoints if not cp.passed]
    assert "CP3" in failed_ids


def test_readability_metrics_calculation():
    stats = analyze_readability(PASSING_LESSON_CONTENT)
    assert stats.total_words > 400
    assert stats.total_sentences > 20
    assert stats.avg_sentence_length < 20.0
    assert stats.has_relatable_analogy is True
    assert stats.has_check_for_understanding is True
