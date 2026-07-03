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

    truck = self.get_available_truck()

    if truck is None:
        print("No truck available.")
        return

    if not self.can_dispatch_now():

        wait = self.simulator.clock.minutes_until_next_work_start()

        print(
            f"Truck movement not allowed."
            f" Wait {wait} minutes."
        )

        return

    self.schedule_departure(tank, truck)
  
  def schedule_departure(self, tank, truck):

    event = Event(
        simulation_time=self.simulator.clock.simulation_time,
        event_type=EventType.TRUCK_DEPARTED,
        truck_head_id=truck.id,
        tank_id=tank.id,
        description=f"Truck {truck.id} departed with Tank {tank.id}."
    )

    self.simulator.event_queue.add_event(event)
  
  def can_dispatch_now(self):

    return self.simulator.clock.is_working_hours()