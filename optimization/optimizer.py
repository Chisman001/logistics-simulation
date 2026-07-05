from optimization.objective import Objective
from optimization.result import OptimizationResult
from optimization.runner import SimulationRunner
from analytics.statistics import Statistics
from analytics.metrics import Metrics
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
      print("Completed deliveries:", statistics.completed_deliveries)
      print("Supply operations:", statistics.supply_operations)
      print("Downtime:", statistics.total_consumer_downtime)
      metrics = Metrics(statistics)

      score = self.objective.calculate_score(
          statistics,
          metrics,
          scenario,
      )

      return OptimizationResult(
          scenario=scenario,
          statistics=statistics,
          score=score,
          metrics=metrics,
      )