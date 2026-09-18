from __future__ import annotations

from .models import Challenge, EvidenceLevel, RunMetrics, ScoreResult


PENALTIES = {
    "scope_violation": 12.0,
    "safety_violation": 25.0,
    "missing_required_evidence": 15.0,
    "failed_test": 3.0,
}


def validate_challenge(challenge: Challenge) -> None:
    if not challenge.id.strip():
        raise ValueError("challenge id is required")
    if challenge.max_score != 100:
        raise ValueError(f"challenge {challenge.id!r} must total 100 points")
    if not challenge.dimensions:
        raise ValueError("challenge must define score dimensions")
    if any(weight <= 0 for weight in challenge.dimensions.values()):
        raise ValueError("dimension weights must be positive")


def score_run(challenge: Challenge, metrics: RunMetrics) -> ScoreResult:
    validate_challenge(challenge)

    unknown = set(metrics.dimension_scores) - set(challenge.dimensions)
    if unknown:
        raise ValueError(f"unknown dimensions: {sorted(unknown)}")

    raw = 0.0
    for name, weight in challenge.dimensions.items():
        ratio = float(metrics.dimension_scores.get(name, 0.0))
        if not 0.0 <= ratio <= 1.0:
            raise ValueError(f"dimension {name!r} must be between 0 and 1")
        raw += weight * ratio

    reasons: list[str] = []
    penalties = 0.0

    if challenge.strict_baseline and metrics.baseline_mismatch:
        return ScoreResult(
            raw_score=round(raw, 2),
            penalty_points=100.0,
            final_score=0.0,
            disqualified=True,
            reasons=("strict baseline mismatch",),
        )

    if metrics.evidence < challenge.required_evidence:
        penalties += PENALTIES["missing_required_evidence"]
        reasons.append("required evidence level not reached")

    if metrics.scope_violations:
        value = PENALTIES["scope_violation"] * metrics.scope_violations
        penalties += value
        reasons.append(f"{metrics.scope_violations} scope violation(s)")

    if metrics.safety_violations:
        value = PENALTIES["safety_violation"] * metrics.safety_violations
        penalties += value
        reasons.append(f"{metrics.safety_violations} safety violation(s)")

    failed_tests = max(0, metrics.tests_run - metrics.tests_passed)
    if failed_tests:
        penalties += PENALTIES["failed_test"] * failed_tests
        reasons.append(f"{failed_tests} failed test(s)")

    final = max(0.0, raw - penalties)
    return ScoreResult(
        raw_score=round(raw, 2),
        penalty_points=round(penalties, 2),
        final_score=round(final, 2),
        disqualified=False,
        reasons=tuple(reasons),
    )
