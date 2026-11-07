"""
Surgical Semantic Diff & Patch Analyzer
Tracks line-by-line additions, deletions, and modifications between drafts.
Calculates token economy and surgical repair efficiency.
"""

import difflib
import re
from typing import List, Dict, Any, Tuple


class SurgicalPatcher:
    """Computes semantic and text-level diffs between iterations."""

    @staticmethod
    def compute_diff(original_text: str, repaired_text: str) -> Dict[str, Any]:
        """
        Calculates a structured diff between two iterations.
        Returns additions, deletions, line diffs, and efficiency stats.
        """
        orig_lines = [line.strip() for line in original_text.splitlines() if line.strip()]
        rep_lines = [line.strip() for line in repaired_text.splitlines() if line.strip()]

        matcher = difflib.SequenceMatcher(None, orig_lines, rep_lines)
        diff_chunks = []
        added_count = 0
        deleted_count = 0
        unchanged_count = 0

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for line in orig_lines[i1:i2]:
                    diff_chunks.append({
                        "type": "unchanged",
                        "text": line
                    })
                    unchanged_count += 1
            elif tag == 'delete':
                for line in orig_lines[i1:i2]:
                    diff_chunks.append({
                        "type": "deleted",
                        "text": line
                    })
                    deleted_count += 1
            elif tag == 'insert':
                for line in rep_lines[j1:j2]:
                    diff_chunks.append({
                        "type": "added",
                        "text": line
                    })
                    added_count += 1
            elif tag == 'replace':
                for line in orig_lines[i1:i2]:
                    diff_chunks.append({
                        "type": "deleted",
                        "text": line
                    })
                    deleted_count += 1
                for line in rep_lines[j1:j2]:
                    diff_chunks.append({
                        "type": "added",
                        "text": line
                    })
                    added_count += 1

        total_lines = added_count + deleted_count + unchanged_count
        preservation_rate = round((unchanged_count / max(1, len(orig_lines))) * 100, 1)

        return {
            "diff_chunks": diff_chunks,
            "lines_added": added_count,
            "lines_deleted": deleted_count,
            "lines_unchanged": unchanged_count,
            "preservation_rate_pct": preservation_rate,
            "total_modifications": added_count + deleted_count
        }

    @staticmethod
    def summarize_changes(diff_data: Dict[str, Any]) -> str:
        """Produces a concise human-readable changelog."""
        added = diff_data.get("lines_added", 0)
        deleted = diff_data.get("lines_deleted", 0)
        preservation = diff_data.get("preservation_rate_pct", 0.0)

        return (
            f"Surgically replaced {deleted} violating lines with {added} clarified lines. "
            f"Preserved {preservation}% of good structural prose from the previous iteration."
        )
