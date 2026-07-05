from optimization.scenerio import Scenario
from optimization.optimizer import Optimizer
from optimization.exporter import OptimizationExporter

class Search:

    def __init__(self):
        self.optimizer = Optimizer()

        self.tank_counts = range(3, 7)
        self.truck_counts = range(2, 6)

        self.travel_times = [75, 90, 105]
        self.fill_times = [90, 120]
        self.safety_windows = [30, 60]

    def search(self):
        raise NotImplementedError
    
    def generate_scenarios(self):

      scenarios = []

      for tanks in self.tank_counts:

          for trucks in self.truck_counts:

              for travel in self.travel_times:

                  for fill in self.fill_times:

                      for safety in self.safety_windows:

                          scenario = Scenario(
                              num_tanks=tanks,
                              num_truck_heads=trucks,
                              tank_capacity=520,
                              tank_duration=480,
                              travel_time=travel,
                              fill_time=fill,
                              safety_window=safety,
                          )

                          scenarios.append(scenario)

      return scenarios
    
    def search(self):

      results = []

      scenarios = self.generate_scenarios()

      for scenario in scenarios:

          result = self.optimizer.evaluate(scenario)

          results.append(result)
          
      results.sort(
        key=lambda result: result.score,
        reverse=True
      )
          
      best = self.find_best_result(results)
      exporter = OptimizationExporter()
      exporter.export(results)

      return best, results
    
    def find_best_result(
    self,
    results,
    ):
      return max(
          results,
          key=lambda result: result.score
      )