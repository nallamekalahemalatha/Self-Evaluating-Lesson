"""
Advanced Engine Test Suite
Tests Grounding Retrieval, Comprehensive Cognitive Readability, Surgical Patching, and Telemetry.
"""

import pytest
from core.grounding import GroundingRetriever
from rubrics.advanced_metrics import compute_comprehensive_metrics
from core.patcher import SurgicalPatcher
from core.pipeline import ContentPipeline
from core.memory import MemoryStore
from core.evolution import EvolutionEngine
from core.mock_engine import PASSING_LESSON_CONTENT, FLAWED_JARGON_CONTENT


def test_grounding_retrieval():
    retriever = GroundingRetriever()
    results = retriever.retrieve("Introduction to RAG", top_k=3)
    assert len(results) == 3
    assert results[0]["similarity_score"] > 0.4
    assert any("Lewis et al" in r["title"] or "Foundation" in r["title"] for r in results)


def test_comprehensive_metrics():
    metrics = compute_comprehensive_metrics(PASSING_LESSON_CONTENT)
    assert "coleman_liau_index" in metrics
    assert "gunning_fog_index" in metrics
    assert "easy_word_percentage" in metrics
    assert "cognitive_accessibility_score" in metrics
    assert "sentence_length_std_dev" in metrics

    # For beginner passing content, easy word % should be >= 55%
    assert metrics["easy_word_percentage"] >= 55.0
    # Cognitive score should be high
    assert metrics["cognitive_accessibility_score"] >= 70.0


def test_surgical_patcher_diff():
    diff_data = SurgicalPatcher.compute_diff(FLAWED_JARGON_CONTENT, PASSING_LESSON_CONTENT)
    assert diff_data["lines_added"] > 0
    assert diff_data["lines_deleted"] > 0
    assert "diff_chunks" in diff_data
    summary = SurgicalPatcher.summarize_changes(diff_data)
    assert "Surgically" in summary


def test_pipeline_telemetry_and_grounding(tmp_path):
    test_db = tmp_path / "telemetry_test.db"
    test_evo = tmp_path / "telemetry_evo.json"
    memory = MemoryStore(db_path=test_db)
    evolution = EvolutionEngine(store_path=test_evo)

    pipeline = ContentPipeline(
        provider="mock",
        max_retries=2,
        memory_store=memory,
        evolution_engine=evolution
    )

    result = pipeline.execute(topic="Introduction to RAG", deliberate_flaw="jargon")
    assert result.is_approved is True
    assert len(result.retrieved_context_chunks) == 3
    assert "total_duration_sec" in result.telemetry
    assert result.telemetry["total_tokens"] > 0
    assert len(result.iteration_diffs) == 1
    assert result.iteration_diffs[0]["from_iteration"] == 1
