from optimization.scenerio import Scenario
from optimization.optimizer import Optimizer

class Search:

    def __init__(self):
        self.optimizer = Optimizer()

    def search(self):
        raise NotImplementedError
    
    def generate_scenarios(self):

      scenarios = []

      for tanks in range(3, 7):

          for trucks in range(2, 5):

              scenario = Scenario(
                  num_tanks=tanks,
                  num_truck_heads=trucks,
                  tank_capacity=520,
                  tank_duration=480,
                  travel_time=90,
                  fill_time=120,
                  safety_window=60,
              )

              scenarios.append(scenario)

      return scenarios
    
    def search(self):

      results = []

      scenarios = self.generate_scenarios()

      for scenario in scenarios:

          result = self.optimizer.evaluate(scenario)

          results.append(result)
          
      best = self.find_best_result(results)

      return best, results
    
    def find_best_result(
    self,
    results,
    ):
      return max(
          results,
          key=lambda result: result.score
      )