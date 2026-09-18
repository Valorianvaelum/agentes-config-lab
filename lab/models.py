from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Mapping


class EvidenceLevel(IntEnum):
    E0 = 0
    E1 = 1
    E2 = 2
    E3 = 3
    E4 = 4


@dataclass(frozen=True)
class Challenge:
    id: str
    title: str
    description: str
    dimensions: Mapping[str, int]
    required_evidence: EvidenceLevel = EvidenceLevel.E3
    strict_baseline: bool = True

    @property
    def max_score(self) -> int:
        return sum(self.dimensions.values())


@dataclass(frozen=True)
class RunMetrics:
    dimension_scores: Mapping[str, float]
    evidence: EvidenceLevel
    duration_seconds: float = 0.0
    cost_usd: float = 0.0
    human_interventions: int = 0
    tests_run: int = 0
    tests_passed: int = 0
    scope_violations: int = 0
    safety_violations: int = 0
    baseline_mismatch: bool = False
    notes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ScoreResult:
    raw_score: float
    penalty_points: float
    final_score: float
    disqualified: bool
    reasons: tuple[str, ...]
