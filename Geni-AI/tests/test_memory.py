"""
Tests for Persistent Memory & Self-Evolution
"""

import pytest
from core.memory import MemoryStore
from core.evolution import EvolutionEngine
from core.state import RejectionLogEntry, PipelineRunResult, EvaluationResult, ReadabilityStats
from datetime import datetime


def test_memory_store_lifecycle(tmp_path):
    test_db = tmp_path / "lifecycle.db"
    store = MemoryStore(db_path=test_db)

    eval_sample = EvaluationResult(
        iteration=1,
        is_passing=True,
        passed_count=6,
        total_count=6,
        checkpoints=[],
        readability=ReadabilityStats(
            flesch_kincaid_grade=6.5,
            avg_sentence_length=14.2,
            total_words=850,
            total_sentences=60
        ),
        overall_critique="Great lesson"
    )

    run_sample = PipelineRunResult(
        run_id="test_run_001",
        topic="Introduction to RAG",
        provider="mock",
        is_approved=True,
        total_iterations=1,
        final_lesson="# Test Content",
        evaluations=[eval_sample],
        rejection_log=[],
        evolved_rules_applied=["Rule 1"],
        newly_evolved_rules=[],
        started_at=datetime.utcnow().isoformat(),
        completed_at=datetime.utcnow().isoformat()
    )

    store.record_run(run_sample)

    runs = store.get_all_runs()
    assert len(runs) == 1
    assert runs[0]["run_id"] == "test_run_001"
    assert runs[0]["is_approved"] == 1


def test_evolution_from_rejection(tmp_path):
    test_evo = tmp_path / "evo.json"
    engine = EvolutionEngine(store_path=test_evo)

    initial_count = len(engine.get_active_guardrails())

    rejection = RejectionLogEntry(
        iteration=1,
        failed_checkpoints=["CP1"],
        root_cause_analysis="Claimed RAG trains weights",
        offending_snippets=["modifies neural network weights"],
        targeted_feedback="Clarify that RAG does not retrain weights",
        action_taken_on_retry="Fixed explanation"
    )

    newly_added = engine.evolve_from_rejections([rejection])
    assert len(newly_added) > 0

    updated_guardrails = engine.get_active_guardrails()
    assert len(updated_guardrails) > initial_count
