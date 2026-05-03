from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build an AI-agent application evidence pack.")
    parser.add_argument("--brief", default="examples/application_brief.md", help="Path to the application brief.")
    parser.add_argument("--out", default="outputs/demo-run", help="Output directory.")
    parser.add_argument("--remote", action="store_true", help="Use AGENTPROOF_* OpenAI-compatible provider if configured.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = run_pipeline(Path(args.brief), Path(args.out), prefer_remote=args.remote)
    print("AgentProof run completed")
    print(f"Provider: {result.run_context.provider_name} / {result.run_context.model_name}")
    print(f"Review score: {result.review_score}/100")
    print("Generated files:")
    for path in result.files:
        print(f"- {path}")


if __name__ == "__main__":
    main()

