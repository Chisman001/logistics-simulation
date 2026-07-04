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