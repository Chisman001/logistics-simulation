from dataclasses import dataclass

from analytics.statistics import Statistics
from optimization.scenerio import Scenario
from analytics.metrics import Metrics


@dataclass
class OptimizationResult:
    scenario: Scenario
    statistics: Statistics
    score: float
    metrics: Metrics