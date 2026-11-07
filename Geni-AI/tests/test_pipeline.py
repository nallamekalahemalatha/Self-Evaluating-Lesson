"""
Tests for Pipeline Closed-Loop Orchestration & Regeneration
"""

import pytest
from core.pipeline import ContentPipeline
from core.memory import MemoryStore
from core.evolution import EvolutionEngine
from pathlib import Path


def test_pipeline_baseline_run_passes(tmp_path):
    test_db = tmp_path / "test_memory.db"
    test_evo = tmp_path / "test_evo.json"
    memory = MemoryStore(db_path=test_db)
    evolution = EvolutionEngine(store_path=test_evo)

    pipeline = ContentPipeline(
        provider="mock",
        max_retries=2,
        memory_store=memory,
        evolution_engine=evolution
    )

    result = pipeline.execute(topic="Introduction to RAG", deliberate_flaw=None)
    assert result.is_approved is True
    assert result.total_iterations == 1
    assert len(result.rejection_log) == 0
    assert len(result.evaluations) == 1
    assert result.evaluations[0].is_passing is True


def test_pipeline_catches_flaw_and_regenerates_successfully(tmp_path):
    test_db = tmp_path / "test_memory.db"
    test_evo = tmp_path / "test_evo.json"
    memory = MemoryStore(db_path=test_db)
    evolution = EvolutionEngine(store_path=test_evo)

    pipeline = ContentPipeline(
        provider="mock",
        max_retries=2,
        memory_store=memory,
        evolution_engine=evolution
    )

    # Injected deliberate flaw: jargon
    result = pipeline.execute(topic="Introduction to RAG", deliberate_flaw="jargon")

    # The pipeline should have rejected iteration 1, triggered retry, and approved iteration 2
    assert result.is_approved is True
    assert result.total_iterations == 2
    assert len(result.rejection_log) == 1
    
    rejection = result.rejection_log[0]
    assert rejection.iteration == 1
    assert len(rejection.failed_checkpoints) > 0
    assert rejection.action_taken_on_retry != ""
    
    # Second evaluation must be approved
    assert result.evaluations[0].is_passing is False
    assert result.evaluations[1].is_passing is True
