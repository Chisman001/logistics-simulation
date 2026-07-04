from optimization.objective import Objective
from optimization.result import OptimizationResult
from optimization.runner import SimulationRunner
from analytics.statistics import Statistics
from optimization.scenerio import Scenario


class Optimizer:

    def __init__(self):
        self.runner = SimulationRunner()
        self.objective = Objective()

    def evaluate(
    self,
    scenario: Scenario,
    ) -> OptimizationResult:
      simulator = self.runner.run(
          scenario
      )

      statistics = simulator.statistics

      score = self.objective.calculate_score(
          statistics,
          scenario,
      )

      return OptimizationResult(
          scenario=scenario,
          statistics=statistics,
          score=score,
      )