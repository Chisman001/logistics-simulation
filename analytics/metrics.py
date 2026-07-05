class Metrics:
  def __init__(self, statistics):
      self.statistics = statistics

  def _average(self, values):

      if not values:
          return 0

      return sum(values) / len(values)

  def _maximum(self, values):
    if not values:
      return 0
    return max(values)
  
  def _minimum(self, values):
    if not values:
      return 0
    return min(values)

  def average_tank_wait(self):
    return self._average(
      self.statistics.tank_wait_times
    )
  
  def average_empty_wait(self):
    return self._average(
      self.statistics.empty_wait_times
    )
  
  def average_delivery_time(self):
    return self._average(
      self.statistics.delivery_times
    )

  def average_cycle_time(self):
    return self._average(
      self.statistics.cycle_times
    )

  def maximum_tank_wait(self):
    return self._maximum(
      self.statistics.tank_wait_times
    ) 

  def minimum_tank_wait(self):
    return self._minimum(
      self.statistics.tank_wait_times
    )

  def _total(self, value):
    return value     
  
  def total_consumer_downtime(self):
    return self._total(
      self.statistics.total_consumer_downtime
    )

  def maximum_safety_delay(self):
    return self._maximum(
      self.statistics.safety_delays
    )
  
  def average_safety_delay(self):
    return self._average(
      self.statistics.safety_delays
    )

  def deliveries_completed(self):
    return self.statistics.completed_deliveries

  def cycles_completed(self):
    return self.statistics.completed_cycles

  def dispatches(self):
    return self.statistics.dispatches

  def returns(self):
    return self.statistics.returns
  
  def simulation_duration(self):
    return self.statistics.simulation_duration
  
  def safety_violations(self):
    return self.statistics.safety_violations

  def total_safety_delay(self):
    return self.statistics.total_safety_delay

  def supply_operations(self):
    return self.statistics.supply_operations

  def average_deliveries_per_day(self, simulation_days):
    if simulation_days == 0:
      return 0
    return self.deliveries_completed() / simulation_days

  def average_supply_starts_per_day(self, simulation_days):
    if simulation_days == 0:
      return 0
    return self.supply_operations() / simulation_days

  def expected_supply_periods(self, config):
    handover_interval = config.TANK_DURATION - config.SAFETY_WINDOW
    if handover_interval == 0:
      return 0
    return self.simulation_duration() / handover_interval

  def simulation_summary(self):
    return {
      "Simulation Duration": self.simulation_duration(),
      "Completed Deliveries": self.deliveries_completed(),
      "Completed Cycles": self.cycles_completed(),
      "Dispatches": self.dispatches(),
      "Returns": self.returns(),
    }

  def tank_performance(self):
    return {
      "Average Tank Wait": self.average_tank_wait(),
      "Maximum Tank Wait": self.maximum_tank_wait(),
      "Minimum Tank Wait": self.minimum_tank_wait(),
      "Average Cycle Time": self.average_cycle_time(),
      "Average Delivery Time": self.average_delivery_time(),
    }

  def fleet_performance(self):
    return {
      "Average Empty Tank Wait": self.average_empty_wait(),
    }

  def safety_metrics(self):
    return {
        "Safety Violations": self.safety_violations(),
        "Total Safety Delay": self.total_safety_delay(),
        "Maximum Safety Delay": self.maximum_safety_delay(),
        "Average Safety Delay": self.average_safety_delay(),
    }

  def consumer_service(self):
    return {
      "Consumer Downtime (reported)": self.total_consumer_downtime(),
    }

  def throughput(self, config):
    days = config.SIMULATION_DAYS
    return {
      "Supply Operations": self.supply_operations(),
      "Average Deliveries/Day": round(self.average_deliveries_per_day(days), 2),
      "Average Supply Starts/Day": round(self.average_supply_starts_per_day(days), 2),
      "Expected Supply Periods": round(self.expected_supply_periods(config), 1),
    }