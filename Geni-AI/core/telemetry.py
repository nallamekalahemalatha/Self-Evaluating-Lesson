"""
Pipeline Telemetry & Execution Monitoring
Measures phase latencies, estimates token usage, and computes cost analytics.
"""

import time
from typing import Dict, Any, Optional


# Pricing benchmarks per 1,000,000 tokens (USD)
PRICING_CATALOG = {
    "gemini": {
        "prompt_cost_per_m": 0.075,
        "completion_cost_per_m": 0.30
    },
    "openai": {
        "prompt_cost_per_m": 0.15,
        "completion_cost_per_m": 0.60
    },
    "mock": {
        "prompt_cost_per_m": 0.0,
        "completion_cost_per_m": 0.0
    }
}


class ExecutionTelemetryTracker:
    def __init__(self, provider: str = "mock"):
        self.provider = provider
        self.start_time = time.perf_counter()
        self.phase_timings: Dict[str, float] = {}
        self.prompt_tokens = 0
        self.completion_tokens = 0

    def record_phase(self, phase_name: str, duration_ms: float):
        """Record elapsed time for a discrete pipeline phase."""
        self.phase_timings[phase_name] = round(duration_ms, 2)

    def record_tokens(self, prompt_text: str, completion_text: str):
        """Estimate token usage using industry standard 4-char per token heuristic."""
        p_tokens = max(1, len(prompt_text) // 4)
        c_tokens = max(1, len(completion_text) // 4)
        self.prompt_tokens += p_tokens
        self.completion_tokens += c_tokens

    def compile_metrics(self) -> Dict[str, Any]:
        """Compile complete latency, token, and cost report."""
        total_duration = round(time.perf_counter() - self.start_time, 2)
        total_tokens = self.prompt_tokens + self.completion_tokens

        pricing = PRICING_CATALOG.get(self.provider, PRICING_CATALOG["mock"])
        prompt_cost = (self.prompt_tokens / 1_000_000) * pricing["prompt_cost_per_m"]
        completion_cost = (self.completion_tokens / 1_000_000) * pricing["completion_cost_per_m"]
        total_cost_usd = round(prompt_cost + completion_cost, 6)

        return {
            "total_duration_sec": total_duration,
            "phase_timings_ms": self.phase_timings,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": total_tokens,
            "estimated_cost_usd": total_cost_usd,
            "provider": self.provider
        }
