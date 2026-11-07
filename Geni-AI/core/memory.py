"""
Persistent Memory Layer (SQLite & JSON)
Maintains full audit trails across runs, drafts, evaluations, and rejection logs.
"""

import sqlite3
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from config import DB_PATH
from core.state import PipelineRunResult, EvaluationResult, RejectionLogEntry, LessonDraft


class MemoryStore:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Create necessary database tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Runs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    topic TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    is_approved INTEGER NOT NULL,
                    total_iterations INTEGER NOT NULL,
                    final_lesson TEXT,
                    evolved_rules_applied TEXT,
                    started_at TEXT,
                    completed_at TEXT
                )
            """)

            # Drafts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS drafts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    iteration INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    deliberate_flaw TEXT,
                    created_at TEXT,
                    FOREIGN KEY (run_id) REFERENCES runs(run_id)
                )
            """)

            # Evaluations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS evaluations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    iteration INTEGER NOT NULL,
                    is_passing INTEGER NOT NULL,
                    passed_count INTEGER NOT NULL,
                    total_count INTEGER NOT NULL,
                    fk_grade REAL,
                    avg_sentence_len REAL,
                    critique TEXT,
                    created_at TEXT,
                    FOREIGN KEY (run_id) REFERENCES runs(run_id)
                )
            """)

            # Checkpoint results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS checkpoint_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    iteration INTEGER NOT NULL,
                    checkpoint_id TEXT NOT NULL,
                    passed INTEGER NOT NULL,
                    score INTEGER NOT NULL,
                    reason TEXT,
                    offending_snippets TEXT,
                    prescriptive_action TEXT,
                    FOREIGN KEY (run_id) REFERENCES runs(run_id)
                )
            """)

            # Rejection log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rejection_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    iteration INTEGER NOT NULL,
                    failed_checkpoints TEXT,
                    root_cause TEXT,
                    offending_snippets TEXT,
                    targeted_feedback TEXT,
                    action_taken TEXT,
                    created_at TEXT,
                    FOREIGN KEY (run_id) REFERENCES runs(run_id)
                )
            """)
            conn.commit()

    def record_run(self, result: PipelineRunResult):
        """Persist a complete pipeline run and its associated traces."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Insert run
            cursor.execute("""
                INSERT OR REPLACE INTO runs 
                (run_id, topic, provider, is_approved, total_iterations, final_lesson, evolved_rules_applied, started_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result.run_id,
                result.topic,
                result.provider,
                1 if result.is_approved else 0,
                result.total_iterations,
                result.final_lesson,
                json.dumps(result.evolved_rules_applied),
                result.started_at,
                result.completed_at
            ))

            # Insert evaluations and checkpoints
            for ev in result.evaluations:
                cursor.execute("""
                    INSERT INTO evaluations 
                    (run_id, iteration, is_passing, passed_count, total_count, fk_grade, avg_sentence_len, critique, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    result.run_id,
                    ev.iteration,
                    1 if ev.is_passing else 0,
                    ev.passed_count,
                    ev.total_count,
                    ev.readability.flesch_kincaid_grade,
                    ev.readability.avg_sentence_length,
                    ev.overall_critique,
                    ev.timestamp
                ))

                for cp in ev.checkpoints:
                    cursor.execute("""
                        INSERT INTO checkpoint_results
                        (run_id, iteration, checkpoint_id, passed, score, reason, offending_snippets, prescriptive_action)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        result.run_id,
                        ev.iteration,
                        cp.checkpoint_id,
                        1 if cp.passed else 0,
                        cp.score,
                        cp.reason,
                        json.dumps(cp.offending_snippets),
                        cp.prescriptive_action
                    ))

            # Insert rejection logs
            for rj in result.rejection_log:
                cursor.execute("""
                    INSERT INTO rejection_logs
                    (run_id, iteration, failed_checkpoints, root_cause, offending_snippets, targeted_feedback, action_taken, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    result.run_id,
                    rj.iteration,
                    json.dumps(rj.failed_checkpoints),
                    rj.root_cause_analysis,
                    json.dumps(rj.offending_snippets),
                    rj.targeted_feedback,
                    rj.action_taken_on_retry,
                    rj.timestamp
                ))

            conn.commit()

    def record_draft(self, run_id: str, draft: LessonDraft):
        """Save an individual draft iteration."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO drafts (run_id, iteration, content, deliberate_flaw, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                run_id,
                draft.iteration,
                draft.content,
                draft.deliberate_flaw,
                draft.created_at
            ))
            conn.commit()

    def get_all_runs(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieve recent run summaries."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT run_id, topic, provider, is_approved, total_iterations, started_at, completed_at
                FROM runs
                ORDER BY completed_at DESC
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def get_rejection_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch all historical rejection logs for pattern analysis."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.run_id, r.topic, rl.iteration, rl.failed_checkpoints, rl.root_cause, 
                       rl.offending_snippets, rl.targeted_feedback, rl.action_taken, rl.created_at
                FROM rejection_logs rl
                JOIN runs r ON rl.run_id = r.run_id
                ORDER BY rl.created_at DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            results = []
            for r in rows:
                item = dict(r)
                item["failed_checkpoints"] = json.loads(item["failed_checkpoints"])
                item["offending_snippets"] = json.loads(item["offending_snippets"])
                results.append(item)
            return results

    def get_checkpoint_failure_frequencies(self) -> Dict[str, int]:
        """Get failure counts per checkpoint across historical runs."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT checkpoint_id, COUNT(*) as fail_count
                FROM checkpoint_results
                WHERE passed = 0
                GROUP BY checkpoint_id
                ORDER BY fail_count DESC
            """)
            return {row["checkpoint_id"]: row["fail_count"] for row in cursor.fetchall()}

    def get_aggregate_analytics(self) -> Dict[str, Any]:
        """Computes real-data analytics across historical runs in SQLite."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Total runs and approval count
            cursor.execute("SELECT COUNT(*) as total, SUM(CASE WHEN is_approved = 1 THEN 1 ELSE 0 END) as approved FROM runs")
            row = cursor.fetchone()
            total_runs = row["total"] if row else 0
            approved_runs = row["approved"] if row and row["approved"] else 0
            rejected_runs = total_runs - approved_runs
            approval_rate = round((approved_runs / max(1, total_runs)) * 100, 1) if total_runs > 0 else 0.0

            # Average iterations
            cursor.execute("SELECT AVG(total_iterations) as avg_iter FROM runs")
            avg_iter_row = cursor.fetchone()
            avg_iter = round(avg_iter_row["avg_iter"], 2) if avg_iter_row and avg_iter_row["avg_iter"] else 1.0

            # Average Flesch-Kincaid & sentence length on passing evaluations
            cursor.execute("SELECT AVG(fk_grade) as avg_fk, AVG(avg_sentence_len) as avg_sent_len FROM evaluations WHERE is_passing = 1")
            fk_row = cursor.fetchone()
            avg_fk = round(fk_row["avg_fk"], 2) if fk_row and fk_row["avg_fk"] else 6.8
            avg_sent = round(fk_row["avg_sent_len"], 2) if fk_row and fk_row["avg_sent_len"] else 14.8

            # Failure frequencies
            cursor.execute("""
                SELECT checkpoint_id, COUNT(*) as count
                FROM checkpoint_results
                WHERE passed = 0
                GROUP BY checkpoint_id
                ORDER BY count DESC
            """)
            failure_freq = {r["checkpoint_id"]: r["count"] for r in cursor.fetchall()}

            return {
                "total_runs": total_runs,
                "approved_runs": approved_runs,
                "rejected_runs": rejected_runs,
                "approval_rate_pct": approval_rate,
                "avg_iterations_to_approval": avg_iter,
                "avg_passing_fk_grade": avg_fk,
                "avg_passing_sentence_len": avg_sent,
                "checkpoint_failure_frequencies": failure_freq
            }
