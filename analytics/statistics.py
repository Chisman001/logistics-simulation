class Statistics:
  def __init__(self):
    # Counters
    self.completed_deliveries = 0
    self.completed_cycles = 0
    self.dispatches = 0
    self.returns = 0
    self.fill_operations = 0
    self.supply_operations = 0

    # Totals
    self.total_truck_travel_time = 0
    self.total_tank_wait_time = 0
    self.total_empty_wait_time = 0
    self.total_consumer_downtime = 0
    self.total_delivery_time = 0

    # Lists
    self.truck_wait_times = []
    self.tank_wait_times = []
    self.empty_wait_times = []
    self.delivery_times = []
    self.cycle_times = []

    # Safety
    self.safety_violations = 0
    self.total_safety_delay = 0

    self.safety_delays = []

  # record dispatch
  def record_dispatch(self):
    self.dispatches += 1

  # record return
  def record_return(self):
    self.returns += 1

  # record filling
  def record_fill(self):
    self.fill_operations += 1

  # record supply
  def record_supply(self):
    self.supply_operations += 1

  # record delivery completion
  def record_delivery_completion(self):
    self.completed_deliveries += 1

  # record completed cycle
  def record_completed_cycle(self):
    self.completed_cycles += 1

  def record_cycle(self, tank):
    if tank.fill_started_at is None or tank.returned_at is None:
      return

    cycle_time = tank.returned_at - tank.fill_started_at
    self.record_cycle_time(cycle_time)

  def record_cycle_time(self, minutes: int):
    self.cycle_times.append(minutes)
    self.record_completed_cycle()

  # Time recording methods
  def record_truck_travel(self, minutes: int):
    self.total_truck_travel_time += minutes

  def record_tank_wait(self, minutes: int):
    self.total_tank_wait_time += minutes 
    self.tank_wait_times.append(minutes)

  def record_delivery_time(self, minutes: int):
    self.total_delivery_time += minutes
    self.delivery_times.append(minutes)

  def record_delivery(self, tank):
    if tank.departed_at is None or tank.empty_at is None:
      return

    delivery_time = tank.empty_at - tank.departed_at
    self.record_delivery_time(delivery_time)
    self.record_delivery_completion()

  def record_customer_downtime(self, minutes: int):
    self.total_consumer_downtime += minutes

  def record_empty_wait(self, minutes: int):
    self.total_empty_wait_time += minutes
    self.empty_wait_times.append(minutes)

  # Safety violations
  def record_safety_violation(self, delay):
    self.safety_violations += 1
    self.total_safety_delay += delay
    self.safety_delays.append(delay)