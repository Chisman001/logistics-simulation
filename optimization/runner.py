from copy import deepcopy

from config import Config
from engine.simulation import Simulator
from analytics.statistics import Statistics
from optimization.scenerio import Scenario


class SimulationRunner:

    def run(
    self,
    scenario: Scenario,
    ) -> Simulator:

      simulator = self._create_simulator(
          scenario
      )

      simulator.run()

      return simulator

    def _create_simulator(
    self,
    scenario: Scenario,
    ) -> Simulator:

      config = self._build_config(
          scenario
      )

      return Simulator(config)

    def _build_config(
        self,
        scenario: Scenario,
    ) -> Config:
        config = deepcopy(Config())

        config.NUM_TANKS = (
            scenario.num_tanks
        )

        config.NUM_TRUCK_HEADS = (
            scenario.num_truck_heads
        )

        config.TANK_CAPACITY = (
            scenario.tank_capacity
        )

        config.TANK_DURATION = (
            scenario.tank_duration
        )

        config.TRAVEL_TIME = (
            scenario.travel_time
        )

        config.FILL_TIME = (
            scenario.fill_time
        )

        config.SAFETY_WINDOW = (
            scenario.safety_window
        )

        config.PRINT_REPORTS = False
        config.PRINT_EVENTS = False
        return config