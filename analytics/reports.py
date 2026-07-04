class Report:
  def __init__(self, metrics, config=None, validation_result=None):
    self.metrics = metrics
    self.config = config
    self.validation_result = validation_result

  def print_section(
    self,
    title,
    values
  ):

    print()

    print("=" * 40)

    print(title)

    print("=" * 40)

    for key, value in values.items():
      print(f"{key}: {value}")

  def print_summary(self):
    self.print_section(
      "Simulation Summary",
      self.metrics.simulation_summary()
    )
    if self.config is not None:
      self.print_section(
        "Throughput",
        self.metrics.throughput(self.config)
      )
    self.print_section(
      "Tank Performance",
      self.metrics.tank_performance()
    )

    self.print_section(
      "Fleet Performance",
      self.metrics.fleet_performance()
    )

    self.print_section(
      "Safety",
      self.metrics.safety_metrics()
    )

    consumer = self.metrics.consumer_service()
    if self.validation_result is not None:
      consumer["Consumer Downtime (validator)"] = (
          self.validation_result.total_gap_minutes
      )
    self.print_section("Consumer Service", consumer)

  def print_baseline_report(self):
    print()
    print("=" * 40)
    print("Baseline Configuration")
    print("=" * 40)

    print(f"Truck Heads: {self.config.NUM_TRUCK_HEADS}")
    print(f"Tanks: {self.config.NUM_TANKS}")
    print(f"Tank Capacity: {self.config.TANK_CAPACITY}")
    print(f"Tank Duration: {self.config.TANK_DURATION} min")
    print(f"Travel Time: {self.config.TRAVEL_TIME} min")
    print(f"Fill Time: {self.config.FILL_TIME} min")
    print(f"Safety Window: {self.config.SAFETY_WINDOW} min")

    print()
    print("This configuration is used as the baseline")
    print("for future optimization comparisons.")