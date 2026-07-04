from dataclasses import dataclass

from analytics.statistics import Statistics
from optimization.scenerio import Scenario


@dataclass
class OptimizationResult:
    scenario: Scenario
    statistics: Statistics
    score: float