import unittest

from lab.catalog import CHALLENGES, by_id
from lab.models import Challenge, EvidenceLevel, RunMetrics
from lab.scoring import PENALTIES, score_run, validate_challenge


class LabTests(unittest.TestCase):
    def test_01_catalog_has_three_challenges(self):
        self.assertEqual(len(CHALLENGES), 3)
        self.assertEqual(
            {c.id for c in CHALLENGES},
            {"repo-triage", "defect-remediation", "delivery-review"},
        )

    def test_02_each_challenge_totals_100_points(self):
        for challenge in CHALLENGES:
            validate_challenge(challenge)
            self.assertEqual(challenge.max_score, 100)

    def test_03_evidence_levels_are_ordered_e0_to_e4(self):
        self.assertLess(EvidenceLevel.E0, EvidenceLevel.E1)
        self.assertLess(EvidenceLevel.E1, EvidenceLevel.E2)
        self.assertLess(EvidenceLevel.E2, EvidenceLevel.E3)
        self.assertLess(EvidenceLevel.E3, EvidenceLevel.E4)

    def test_04_perfect_run_scores_100(self):
        challenge = by_id("defect-remediation")
        result = score_run(
            challenge,
            RunMetrics(
                dimension_scores={name: 1.0 for name in challenge.dimensions},
                evidence=EvidenceLevel.E4,
                tests_run=8,
                tests_passed=8,
            ),
        )
        self.assertEqual(result.final_score, 100.0)
        self.assertFalse(result.disqualified)

    def test_05_missing_evidence_is_penalized(self):
        challenge = by_id("delivery-review")
        result = score_run(
            challenge,
            RunMetrics(
                dimension_scores={name: 1.0 for name in challenge.dimensions},
                evidence=EvidenceLevel.E1,
            ),
        )
        self.assertEqual(result.penalty_points, PENALTIES["missing_required_evidence"])
        self.assertEqual(result.final_score, 85.0)

    def test_06_scope_and_failed_tests_accumulate_penalties(self):
        challenge = by_id("defect-remediation")
        result = score_run(
            challenge,
            RunMetrics(
                dimension_scores={name: 1.0 for name in challenge.dimensions},
                evidence=EvidenceLevel.E3,
                scope_violations=1,
                tests_run=8,
                tests_passed=6,
            ),
        )
        expected = PENALTIES["scope_violation"] + 2 * PENALTIES["failed_test"]
        self.assertEqual(result.penalty_points, expected)
        self.assertEqual(result.final_score, 100.0 - expected)

    def test_07_strict_baseline_mismatch_disqualifies(self):
        challenge = by_id("repo-triage")
        result = score_run(
            challenge,
            RunMetrics(
                dimension_scores={name: 1.0 for name in challenge.dimensions},
                evidence=EvidenceLevel.E4,
                baseline_mismatch=True,
            ),
        )
        self.assertTrue(result.disqualified)
        self.assertEqual(result.final_score, 0.0)
        self.assertIn("strict baseline mismatch", result.reasons)

    def test_08_unknown_dimension_is_rejected(self):
        challenge = by_id("repo-triage")
        with self.assertRaises(ValueError):
            score_run(
                challenge,
                RunMetrics(
                    dimension_scores={"invented": 1.0},
                    evidence=EvidenceLevel.E4,
                ),
            )


if __name__ == "__main__":
    unittest.main()
