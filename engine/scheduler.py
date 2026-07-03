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

  def on_tank_ready(self, tank):

    available = self.simulator.get_available_trucks()

    if not available:
      print("No truck heads available.")
      return

    if not self.simulator.clock.is_working_hours():

      wait = self.simulator.clock.minutes_until_next_work_start()

      print(
        f"Truck movement not allowed. "
        f"Waiting {wait} minutes."
      )

      return

    print(
      f"Truck {available[0].id} can transport Tank {tank.id}."
    )