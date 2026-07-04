import unittest

from analytics.statistics import Statistics
from analytics.validator import (
    SimulationValidator,
    compute_coverage_gaps,
    find_overlap_violations,
)
from config import Config


class ValidatorTests(unittest.TestCase):
    def test_no_gaps_when_fully_covered(self):
        intervals = [{"tank_id": 1, "start": 0, "end": 480, "arrived_at": 0}]
        total, periods = compute_coverage_gaps(intervals, 480, 480)
        self.assertEqual(total, 0)
        self.assertEqual(periods, [])

    def test_single_gap(self):
        intervals = [{"tank_id": 1, "start": 60, "end": 600, "arrived_at": 0}]
        total, periods = compute_coverage_gaps(intervals, 600, 480)
        self.assertEqual(total, 60)
        self.assertEqual(periods, [(0, 60)])

    def test_overlap_within_safety_window_is_ok(self):
        intervals = [
            {"tank_id": 1, "start": 0, "end": 480, "arrived_at": 0},
            {"tank_id": 2, "start": 420, "end": 900, "arrived_at": 400},
        ]
        violations = find_overlap_violations(intervals, 60, 480)
        self.assertEqual(violations, [])

    def test_overlap_exceeding_safety_window(self):
        intervals = [
            {"tank_id": 1, "start": 0, "end": 480, "arrived_at": 0},
            {"tank_id": 2, "start": 360, "end": 840, "arrived_at": 300},
        ]
        violations = find_overlap_violations(intervals, 60, 480)
        self.assertEqual(len(violations), 1)
        self.assertGreater(violations[0]["overlap"], 60)

    def test_starts_vs_empties_passes_within_one(self):
        stats = Statistics()
        stats.supply_operations = 6
        stats.completed_deliveries = 5
        stats.simulation_duration = 2880
        stats.supply_intervals = []

        validator = SimulationValidator(stats, Config())
        result = validator.validate()
        starts_check = next(c for c in result.checks if c["name"] == "Starts vs empties")
        self.assertTrue(starts_check["passed"])

    def test_starts_vs_empties_fails_when_far_apart(self):
        stats = Statistics()
        stats.supply_operations = 10
        stats.completed_deliveries = 5
        stats.simulation_duration = 2880
        stats.supply_intervals = []

        validator = SimulationValidator(stats, Config())
        result = validator.validate()
        starts_check = next(c for c in result.checks if c["name"] == "Starts vs empties")
        self.assertFalse(starts_check["passed"])


if __name__ == "__main__":
    unittest.main()
