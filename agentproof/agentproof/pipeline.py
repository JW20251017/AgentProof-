from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .agents import EvidenceAgent, DraftAgent, IntakeAgent, PlannerAgent, ReviewerAgent
from .models import AgentResult, PipelineResult, RunContext
from .providers import build_provider


def write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def as_markdown_log(results: list[AgentResult]) -> str:
    sections = ["# AgentProof Workflow Log", ""]
    for result in results:
        sections.extend(
            [
                f"## {result.name}",
                "",
                f"Objective: {result.objective}",
                "",
                "Metrics:",
                "",
                "```json",
                json.dumps(result.metrics, ensure_ascii=False, indent=2),
                "```",
                "",
                "Output:",
                "",
                result.output,
                "",
            ]
        )
    return "\n".join(sections).strip() + "\n"


def run_pipeline(brief_path: Path, output_dir: Path, prefer_remote: bool = False) -> PipelineResult:
    provider = build_provider(prefer_remote=prefer_remote)
    brief = brief_path.read_text(encoding="utf-8")
    context = RunContext(
        brief_path=brief_path,
        output_dir=output_dir,
        started_at=datetime.now(),
        provider_name=provider.config.name,
        model_name=provider.config.model,
    )

    agents = [IntakeAgent(), PlannerAgent(), DraftAgent(), EvidenceAgent(), ReviewerAgent()]
    results: list[AgentResult] = []
    for agent in agents:
        results.append(agent.run(brief, results, provider))

    final_answer = next(item.output for item in results if item.name == "DraftAgent")
    review = next(item for item in results if item.name == "ReviewerAgent")
    review_score = int(review.metrics.get("review_score", 0))

    files = [
        write_text(output_dir / "application_answer.md", final_answer + "\n"),
        write_text(output_dir / "workflow_log.md", as_markdown_log(results)),
        write_text(output_dir / "evidence_checklist.md", next(item.output for item in results if item.name == "EvidenceAgent") + "\n"),
        write_text(
            output_dir / "run_manifest.json",
            json.dumps(
                {
                    "started_at": context.started_at.isoformat(timespec="seconds"),
                    "brief_path": str(context.brief_path),
                    "provider": context.provider_name,
                    "model": context.model_name,
                    "review_score": review_score,
                    "outputs": [str(output_dir / name) for name in ["application_answer.md", "workflow_log.md", "evidence_checklist.md"]],
                    "agents": [
                        {
                            "name": item.name,
                            "objective": item.objective,
                            "metrics": item.metrics,
                        }
                        for item in results
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
        ),
    ]

    return PipelineResult(context, results, final_answer, review_score, files)

