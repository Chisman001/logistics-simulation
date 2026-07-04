from collections import deque

from engine.event import Event
from models.enums import EventType

class Scheduler:
  def __init__(self, simulator):
    self.simulator = simulator

    # Tanks waiting at Point A
    self.waiting_full_tanks = deque()

    # Empty tanks waiting at Point C
    self.waiting_empty_tanks = deque()

    # Truck heads available at Point A
    self.available_trucks_at_a = deque()

    # Truck heads available at Point C
    self.available_trucks_at_c = deque()

  def status(self):
    print("Scheduler Status")
    print("----------------")
    print(f"Tanks: {len(self.simulator.tanks)}")
    print(f"Truck Heads: {len(self.simulator.truck_heads)}")
    print(f"Time: {self.simulator.clock.get_date_time()}")

  def schedule_initial_events(self):
    for tank in self.simulator.tanks.values():
      event = Event(
        simulation_time=0,
        event_type=EventType.TANK_FILL_STARTED,
        tank_id=tank.id,
        description=f"Tank {tank.id} started filling."
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

  def on_truck_available(self, truck):

    print(f"Truck {truck.id} is available.")

  def truck_available_at_a(self, truck):

    if truck.id not in self.available_trucks_at_a:
      self.available_trucks_at_a.append(truck.id)
      print(f"Scheduler: Truck {truck.id} available at Point A.")

    self.try_dispatch()

  def truck_available_at_c(self, truck):

    if truck.id not in self.available_trucks_at_c:
      self.available_trucks_at_c.append(truck.id)
      print(f"Scheduler: Truck {truck.id} available at Point C.")

    self.try_return()

  def tank_ready(self, tank):

    if tank.id not in self.waiting_full_tanks:
      self.waiting_full_tanks.append(tank.id)
      print(f"Scheduler: Tank {tank.id} ready.")

    self.try_dispatch()

  def tank_empty(self, tank):

    if tank.id not in self.waiting_empty_tanks:
        self.waiting_empty_tanks.append(tank.id)
        print(f"Scheduler: Tank {tank.id} empty at Point C.")

    self.try_return()

  def try_dispatch(self):

    # No tanks waiting
    if not self.waiting_full_tanks:
        return

    # No trucks waiting
    if not self.available_trucks_at_a:
        return

    # Trucks can't move now
    if not self.can_dispatch_now():
        return

    tank_id = self.waiting_full_tanks.popleft()
    truck_id = self.available_trucks_at_a.popleft()

    tank = self.simulator.tanks[tank_id]
    truck = self.simulator.truck_heads[truck_id]

    self.schedule_departure(tank, truck)


  def try_return(self):
    pass
