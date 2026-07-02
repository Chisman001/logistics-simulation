class Scheduler:
  def __init__(self, simulator):
    self.simulator = simulator

  def status(self):
    print("Scheduler Status")
    print("----------------")
    print(f"Tanks: {len(self.simulator.tanks)}")
    print(f"Truck Heads: {len(self.simulator.truck_heads)}")
    print(f"Time: {self.simulator.clock.get_date_time()}")