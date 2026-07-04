from analytics.statistics import Statistics
from optimization.scenerio import Scenario
from analytics.metrics import Metrics

class Objective:

    def calculate_score(
        self,
        statistics: Statistics,
        metrics: Metrics,
        scenario: Scenario,
    ) -> float:
        score = 100.0

        score -= self._downtime_penalty(statistics)

        score -= self._safety_penalty(statistics)

        score -= self._resource_penalty(scenario)

        score -= self._tank_wait_penalty(metrics)

        score -= self._empty_wait_penalty(metrics)

        return round(max(score, 0), 2)

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
        metrics: Metrics,
    ) -> float:
        tank = metrics.tank_performance()
        return (
            tank['Average Tank Wait']
            * 0.01
        )

    def _empty_wait_penalty(
        self,
        metrics: Metrics,
    ) -> float:
        fleet = metrics.fleet_performance()
        return (
            fleet['Average Empty Tank Wait']
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