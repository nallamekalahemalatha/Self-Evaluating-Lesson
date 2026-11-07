"""
CLI Entrypoint for Self-Evaluating RAG Lesson Content Generator
Interactive console dashboard with Rich formatting, telemetry, grounding trace, and error injection.
"""

import argparse
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

from config import DEFAULT_TOPIC, DEFAULT_PROVIDER
from core.pipeline import ContentPipeline
from core.state import PipelineRunResult


if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console()


def render_banner():
    banner = """
    +---------------------------------------------------------------------------+
    |           SELF-EVALUATING RAG LESSON CONTENT GENERATOR                    |
    |   Autonomous Multi-Inspector Closed Loop with Grounding & Self-Evolution  |
    +---------------------------------------------------------------------------+
    """
    console.print(f"[bold cyan]{banner}[/bold cyan]")


def display_results(result: PipelineRunResult):
    console.print("\n")
    status_color = "bold green" if result.is_approved else "bold red"
    status_label = "APPROVED (READY TO SHIP)" if result.is_approved else "REJECTED (NEEDS REVISION)"
    
    # 1. Execution Summary Panel
    tel = result.telemetry
    summary_panel = Panel(
        f"[bold]Run ID:[/bold] {result.run_id}\n"
        f"[bold]Topic:[/bold] {result.topic}\n"
        f"[bold]Target Persona:[/bold] {result.target_persona}\n"
        f"[bold]Inference Provider:[/bold] {result.provider}\n"
        f"[bold]Total Iterations:[/bold] {result.total_iterations}\n"
        f"[bold]Status:[/bold] [{status_color}]{status_label}[/{status_color}]\n"
        f"[bold]Execution Duration:[/bold] {tel.get('total_duration_sec', 'N/A')}s\n"
        f"[bold]Total Tokens:[/bold] {tel.get('total_tokens', 0):,} | [bold]Estimated Cost:[/bold] ${tel.get('estimated_cost_usd', 0.0):.5f}\n"
        f"[bold]Evolved Guardrails Active:[/bold] {len(result.evolved_rules_applied)}\n"
        f"[bold]Newly Evolved Rules:[/bold] {len(result.newly_evolved_rules)}",
        title="[bold yellow]Pipeline Execution & Telemetry Summary[/bold yellow]",
        border_style="cyan"
    )
    console.print(summary_panel)

    # 2. Grounding Retrieval Trace Table
    if result.retrieved_context_chunks:
        g_table = Table(title="[bold blue]Grounding Retrieval Trace (Using RAG to Teach RAG)[/bold blue]")
        g_table.add_column("Chunk ID", style="cyan", no_wrap=True)
        g_table.add_column("Title", style="white")
        g_table.add_column("Confidence", justify="center", style="green")
        g_table.add_column("Source", style="dim")

        for chunk in result.retrieved_context_chunks:
            g_table.add_row(
                chunk["chunk_id"],
                chunk["title"],
                f"{chunk['similarity_score'] * 100:.0f}%",
                chunk["source"][:45] + "..."
            )
        console.print(g_table)
        console.print("")

    # 3. Evaluations Breakdown
    for ev in result.evaluations:
        table = Table(title=f"Evaluation Iteration {ev.iteration} (Passed {ev.passed_count}/{ev.total_count})")
        table.add_column("Checkpoint", style="cyan", no_wrap=True)
        table.add_column("Dimension", style="magenta")
        table.add_column("Verdict", justify="center")
        table.add_column("Score", justify="center")
        table.add_column("Inspector Justification", style="white")

        for cp in ev.checkpoints:
            verdict = "[green]PASS[/green]" if cp.passed else "[red]FAIL[/red]"
            score_str = f"[bold green]1[/bold green]" if cp.score == 1 else f"[bold red]0[/bold red]"
            table.add_row(cp.checkpoint_id, cp.dimension, verdict, score_str, cp.reason)

        console.print(table)
        
        # Multi-Index Readability Banner
        r = ev.readability
        console.print(
            f"[bold]Cognitive Metrics:[/bold] "
            f"Flesch-Kincaid: [cyan]Grade {r.flesch_kincaid_grade}[/cyan] | "
            f"Coleman-Liau: [cyan]Grade {r.coleman_liau_index}[/cyan] | "
            f"Gunning-Fog: [cyan]{r.gunning_fog_index}[/cyan] | "
            f"Easy Words: [green]{r.easy_word_percentage}%[/green] | "
            f"Cognitive Score: [bold green]{r.cognitive_accessibility_score}/100[/bold green] | "
            f"Avg Sentence Length: {r.avg_sentence_length} words (StdDev: ±{r.sentence_length_std_dev})\n"
        )

    # 4. Surgical Diff Summary
    if result.iteration_diffs:
        console.print("[bold yellow]== Surgical Self-Repair & Semantic Diffs ==[/bold yellow]")
        for item in result.iteration_diffs:
            diff = item["diff"]
            console.print(
                f"[bold cyan]Iteration {item['from_iteration']} -> {item['to_iteration']}:[/bold cyan] "
                f"Added {diff['lines_added']} lines, Removed {diff['lines_deleted']} lines, "
                f"Preserved {diff['preservation_rate_pct']}% of structure."
            )
            console.print(f"[dim]{item['summary']}[/dim]\n")

    # 5. Rejection Audit Log
    if result.rejection_log:
        console.print("[bold red]== Rejection & Correction Audit Log ==[/bold red]")
        for rj in result.rejection_log:
            rj_panel = Panel(
                f"[bold red]Iteration {rj.iteration} Rejected Checkpoints:[/bold red] {', '.join(rj.failed_checkpoints)}\n\n"
                f"[bold]Root Cause Analysis:[/bold]\n{rj.root_cause_analysis}\n\n"
                f"[bold]Targeted Prescriptive Feedback Given to Regenerator:[/bold]\n{rj.targeted_feedback}\n\n"
                f"[bold green]Action Taken on Retry:[/bold green]\n{rj.action_taken_on_retry}",
                title=f"[red]Rejection #{rj.iteration}[/red]",
                border_style="red"
            )
            console.print(rj_panel)

    # 6. Final Lesson Preview
    console.print("\n[bold green]== Final Cleared Lesson ==[/bold green]")
    console.print(Panel(Markdown(result.final_lesson), title="[bold green]Final Passing Content[/bold green]", border_style="green"))


def main():
    parser = argparse.ArgumentParser(description="Self-Evaluating RAG Lesson Content Generator CLI")
    parser.add_argument("--topic", type=str, default=DEFAULT_TOPIC, help="Lesson topic to generate")
    parser.add_argument("--provider", type=str, choices=["mock", "gemini", "openai"], default="mock", help="Inference provider")
    parser.add_argument("--retries", type=int, default=2, help="Maximum allowed retries (1-2)")
    parser.add_argument("--inject-flaw", type=str, choices=["jargon", "hallucination", "no_analogy"], default=None,
                        help="Inject deliberate error for Loom video evaluation demo")
    
    args = parser.parse_args()

    render_banner()

    console.print(f"[bold]Target Persona:[/bold] Indian 12th-grade graduate (non-English medium background)")
    console.print(f"[bold]Topic:[/bold] {args.topic}")
    console.print(f"[bold]Execution Provider:[/bold] {args.provider}")
    if args.inject_flaw:
        console.print(f"[bold red]Deliberate Flaw Injection Active:[/bold red] {args.inject_flaw.upper()} (Evaluator Stress Test)\n")
    else:
        console.print("[bold green]Standard Autonomous Production Run[/bold green]\n")

    pipeline = ContentPipeline(provider=args.provider, max_retries=args.retries)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("[cyan]Initializing pipeline...", total=None)

        def on_status(stage: str, msg: str):
            progress.update(task, description=f"[{stage}] {msg}")
            console.print(f"[dim][{stage}][/dim] {msg}")

        result = pipeline.execute(
            topic=args.topic,
            deliberate_flaw=args.inject_flaw,
            status_callback=on_status
        )

    display_results(result)


if __name__ == "__main__":
    main()
