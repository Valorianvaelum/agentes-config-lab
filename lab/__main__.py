from __future__ import annotations

import argparse
import json

from .catalog import CHALLENGES
from .models import EvidenceLevel, RunMetrics
from .scoring import score_run, validate_challenge


def validate() -> int:
    for challenge in CHALLENGES:
        validate_challenge(challenge)
    print(f"validated {len(CHALLENGES)} challenge(s)")
    return 0


def simulate() -> int:
    results = []
    for challenge in CHALLENGES:
        metrics = RunMetrics(
            dimension_scores={name: 0.8 for name in challenge.dimensions},
            evidence=max(challenge.required_evidence, EvidenceLevel.E3),
            duration_seconds=120.0,
            cost_usd=0.25,
            human_interventions=1,
            tests_run=8,
            tests_passed=8,
        )
        score = score_run(challenge, metrics)
        results.append(
            {
                "challenge": challenge.id,
                "raw_score": score.raw_score,
                "penalty_points": score.penalty_points,
                "final_score": score.final_score,
                "disqualified": score.disqualified,
                "duration_seconds": metrics.duration_seconds,
                "cost_usd": metrics.cost_usd,
                "human_interventions": metrics.human_interventions,
            }
        )
    print(json.dumps(results, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Isolated agent evaluation lab")
    parser.add_argument("command", choices=("validate", "simulate"))
    args = parser.parse_args()
    return validate() if args.command == "validate" else simulate()


if __name__ == "__main__":
    raise SystemExit(main())
