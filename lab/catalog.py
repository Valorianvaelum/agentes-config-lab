from __future__ import annotations

from .models import Challenge, EvidenceLevel


CHALLENGES = (
    Challenge(
        id="repo-triage",
        title="Repository triage and change plan",
        description=(
            "Inspect the real repository state, identify affected architecture, rules, risks "
            "and tests, then produce an evidence-backed implementation plan without modifying production."
        ),
        dimensions={
            "state_inspection": 25,
            "architecture": 20,
            "business_rules": 20,
            "risk_control": 15,
            "test_strategy": 10,
            "handoff_quality": 10,
        },
        required_evidence=EvidenceLevel.E2,
    ),
    Challenge(
        id="defect-remediation",
        title="Scoped defect remediation",
        description=(
            "Correct a bounded defect while preserving existing invariants, adding or updating tests, "
            "and avoiding unrelated refactors or unsafe changes."
        ),
        dimensions={
            "root_cause": 20,
            "correctness": 30,
            "regression_safety": 20,
            "scope_control": 15,
            "test_quality": 15,
        },
        required_evidence=EvidenceLevel.E3,
    ),
    Challenge(
        id="delivery-review",
        title="Delivery review and handoff",
        description=(
            "Review a completed delivery against its objective, diff, architecture, permissions, "
            "security, data integrity, UX, tests and Git state; distinguish technical, functional and visual validation."
        ),
        dimensions={
            "objective_fit": 20,
            "diff_review": 20,
            "security_integrity": 20,
            "regression_analysis": 15,
            "ux_validation": 10,
            "evidence_quality": 15,
        },
        required_evidence=EvidenceLevel.E3,
    ),
)


def by_id(challenge_id: str) -> Challenge:
    for challenge in CHALLENGES:
        if challenge.id == challenge_id:
            return challenge
    raise KeyError(challenge_id)
