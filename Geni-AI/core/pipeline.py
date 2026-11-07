"""
Agentic Pipeline Orchestrator
Manages the Generate -> Evaluate -> Regenerate closed loop with persistent memory and self-evolution.
"""

import uuid
import time
from datetime import datetime
from typing import Optional, List, Callable, Dict, Any
from config import MAX_RETRIES, DEFAULT_PROVIDER, DEFAULT_TOPIC
from core.state import PipelineRunResult, LessonDraft, EvaluationResult, RejectionLogEntry
from core.generator import GeneratorAgent
from core.evaluator import EvaluatorEngine
from core.regenerator import RegeneratorAgent
from core.memory import MemoryStore
from core.evolution import EvolutionEngine
from core.grounding import GroundingRetriever
from core.telemetry import ExecutionTelemetryTracker
from core.patcher import SurgicalPatcher


class ContentPipeline:
    def __init__(
        self,
        provider: Optional[str] = None,
        max_retries: int = MAX_RETRIES,
        memory_store: Optional[MemoryStore] = None,
        evolution_engine: Optional[EvolutionEngine] = None
    ):
        self.provider = provider or DEFAULT_PROVIDER
        self.max_retries = max_retries
        self.memory = memory_store or MemoryStore()
        self.evolution = evolution_engine or EvolutionEngine()
        self.grounding_retriever = GroundingRetriever()
        
        # Sub-agents
        self.generator = GeneratorAgent(provider=self.provider)
        self.evaluator = EvaluatorEngine(provider=self.provider)
        self.regenerator = RegeneratorAgent(provider=self.provider)

    def execute(
        self,
        topic: str = DEFAULT_TOPIC,
        deliberate_flaw: Optional[str] = None,
        status_callback: Optional[Callable[[str, str], None]] = None,
        target_persona: str = "12th-Grade Graduate from India (Non-English Medium Background)"
    ) -> PipelineRunResult:
        """
        Execute the end-to-end self-evaluating generation loop with telemetry and grounding.
        """
        run_id = f"run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        started_at = datetime.utcnow().isoformat()
        telemetry_tracker = ExecutionTelemetryTracker(provider=self.provider)
        
        def notify(stage: str, message: str):
            if status_callback:
                status_callback(stage, message)

        notify("START", f"Starting generation run '{run_id}' for topic: '{topic}'")

        # 1. Grounding Retrieval (Using RAG to teach RAG)
        t_ret_start = time.perf_counter()
        notify("RETRIEVAL", f"Searching verified Knowledge Base for authoritative '{topic}' grounding chunks...")
        grounding_chunks = self.grounding_retriever.retrieve(query=topic, top_k=3)
        telemetry_tracker.record_phase("retrieval_ms", (time.perf_counter() - t_ret_start) * 1000)
        notify("AUGMENT", f"Context augmented with {len(grounding_chunks)} verified domain chunks.")

        # 2. Hydrate Evolved Guardrails from Memory
        t_mem_start = time.perf_counter()
        active_guardrails = self.evolution.get_active_guardrails()
        telemetry_tracker.record_phase("memory_hydration_ms", (time.perf_counter() - t_mem_start) * 1000)
        notify("MEMORY", f"Loaded {len(active_guardrails)} active evolved guardrails from memory store.")

        # 3. Initial Generation (Iteration 1)
        t_gen_start = time.perf_counter()
        notify("GENERATE", f"Generating draft iteration 1 (flaw injection: {deliberate_flaw or 'None'})...")
        current_draft = self.generator.generate(
            topic=topic,
            iteration=1,
            evolved_guardrails=active_guardrails,
            deliberate_flaw=deliberate_flaw
        )
        telemetry_tracker.record_phase("generation_iter1_ms", (time.perf_counter() - t_gen_start) * 1000)
        telemetry_tracker.record_tokens(topic, current_draft.content)
        self.memory.record_draft(run_id, current_draft)

        evaluations: List[EvaluationResult] = []
        rejection_logs: List[RejectionLogEntry] = []
        iteration_diffs: List[Dict[str, Any]] = []
        is_approved = False

        # 4. Multi-Inspector Evaluation & Surgical Regeneration Loop
        iteration = 1
        max_total_iterations = 1 + self.max_retries

        while iteration <= max_total_iterations:
            t_eval_start = time.perf_counter()
            notify("EVALUATE", f"Evaluating draft iteration {iteration} against 6-point hard rubric...")
            eval_result = self.evaluator.evaluate(
                topic=topic,
                lesson_content=current_draft.content,
                iteration=iteration
            )
            telemetry_tracker.record_phase(f"evaluation_iter{iteration}_ms", (time.perf_counter() - t_eval_start) * 1000)
            evaluations.append(eval_result)

            if eval_result.is_passing:
                notify("PASS", f"Draft iteration {iteration} PASSED all {eval_result.total_count} hard checkpoints! Ship ready.")
                is_approved = True
                break
            else:
                failed_count = eval_result.total_count - eval_result.passed_count
                notify("REJECT", f"Draft iteration {iteration} FAILED {failed_count} checkpoint(s). Quality bar not met.")

                # If retries remain, synthesize feedback and regenerate
                if iteration < max_total_iterations:
                    t_regen_start = time.perf_counter()
                    notify("REGENERATE", f"Feeding critique back to Regenerator Agent (Retry {iteration}/{self.max_retries})...")
                    repaired_draft, rejection_entry = self.regenerator.regenerate(
                        topic=topic,
                        failed_draft=current_draft,
                        evaluation=eval_result
                    )
                    telemetry_tracker.record_phase(f"regeneration_iter{iteration}_ms", (time.perf_counter() - t_regen_start) * 1000)
                    telemetry_tracker.record_tokens(current_draft.content, repaired_draft.content)

                    # Compute semantic diff between drafts
                    diff_data = SurgicalPatcher.compute_diff(current_draft.content, repaired_draft.content)
                    iteration_diffs.append({
                        "from_iteration": iteration,
                        "to_iteration": iteration + 1,
                        "diff": diff_data,
                        "summary": SurgicalPatcher.summarize_changes(diff_data)
                    })

                    rejection_logs.append(rejection_entry)
                    current_draft = repaired_draft
                    self.memory.record_draft(run_id, current_draft)
                    iteration += 1
                else:
                    notify("MAX_RETRIES", "Maximum allowed retries exhausted. Terminating loop safely.")
                    break

        completed_at = datetime.utcnow().isoformat()

        # 5. Self-Evolution: Learn from rejections across runs
        newly_evolved = []
        if rejection_logs:
            notify("EVOLUTION", "Extracting failure patterns from rejection log to evolve future guardrails...")
            newly_evolved = self.evolution.evolve_from_rejections(rejection_logs)
            if newly_evolved:
                notify("EVOLUTION", f"Synthesized {len(newly_evolved)} new guardrails for future runs.")

        # 6. Compile Final Result with Telemetry
        telemetry_report = telemetry_tracker.compile_metrics()
        run_result = PipelineRunResult(
            run_id=run_id,
            topic=topic,
            provider=self.provider,
            is_approved=is_approved,
            total_iterations=iteration,
            final_lesson=current_draft.content,
            evaluations=evaluations,
            rejection_log=rejection_logs,
            evolved_rules_applied=active_guardrails,
            newly_evolved_rules=newly_evolved,
            retrieved_context_chunks=grounding_chunks,
            iteration_diffs=iteration_diffs,
            telemetry=telemetry_report,
            target_persona=target_persona,
            started_at=started_at,
            completed_at=completed_at
        )

        # 7. Record run into persistent SQLite store
        self.memory.record_run(run_result)
        notify("DONE", f"Run complete. Status: {'APPROVED' if is_approved else 'UNAPPROVED'}. Persisted to database.")

        return run_result
