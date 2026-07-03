from engine.event import Event
from models.enums import EventType

class Scheduler:
  def __init__(self, simulator):
    self.simulator = simulator
    from engine.event_queue import EventQueue
    self.event_queue = EventQueue()

  def status(self):
    print("Scheduler Status")
    print("----------------")
    print(f"Tanks: {len(self.simulator.tanks)}")
    print(f"Truck Heads: {len(self.simulator.truck_heads)}")
    print(f"Time: {self.simulator.clock.get_date_time()}")

  def schedule_initial_events(self):
    event = Event(
      simulation_time=0,
      event_type=EventType.TANK_FILL_STARTED,
      resource_id=1,
      description="Tank 1 started filling."
    )

    self.simulator.event_queue.add_event(event)