from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class AgentResult:
    name: str
    objective: str
    output: str
    metrics: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RunContext:
    brief_path: Path
    output_dir: Path
    started_at: datetime
    provider_name: str
    model_name: str


@dataclass(frozen=True)
class PipelineResult:
    run_context: RunContext
    results: list[AgentResult]
    final_answer: str
    review_score: int
    files: list[Path]

