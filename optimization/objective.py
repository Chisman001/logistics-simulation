from analytics.statistics import Statistics
from optimization.scenerio import Scenario

class Objective:

    def calculate_score(
        self,
        statistics: Statistics,
        scenario: Scenario,
    ) -> float:
        score = 100.0

        score -= self._downtime_penalty(statistics)

        score -= self._safety_penalty(statistics)

        score -= self._tank_wait_penalty(statistics)

        score -= self._empty_wait_penalty(statistics)

        score -= self._resource_penalty(scenario)

        return max(score, 0)

    def _downtime_penalty(
        self,
        statistics: Statistics,
    ) -> float:
        return (
            statistics.total_consumer_downtime
            * 0.10
        )

    def _safety_penalty(
        self,
        statistics: Statistics,
    ) -> float:
        return (
            statistics.safety_violations
            * 25
        )

    def _tank_wait_penalty(
        self,
        statistics: Statistics,
    ) -> float:
        return (
            statistics.average_tank_wait()
            * 0.01
        )

    def _empty_wait_penalty(
        self,
        statistics: Statistics,
    ) -> float:
        return (
            statistics.average_empty_tank_wait()
            * 0.01
        )

    def _resource_penalty(
        self,
        scenario: Scenario,
    ) -> float:
        return (
            scenario.num_tanks * 2
            + scenario.num_truck_heads * 5
        )