from collections import deque

from engine.event import Event
from models.enums import EventType, TruckState, TankState

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
    self.workday_start_scheduled = False
    self.dispatch_ready_scheduled = False

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
    self.tank_ready(tank)
  
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
      self.simulator.log(f"Scheduler: Truck {truck.id} available at Point A.")

    self.try_dispatch()

  def truck_available_at_c(self, truck):

    if truck.id not in self.available_trucks_at_c:
      self.available_trucks_at_c.append(truck.id)
      self.simulator.log(f"Scheduler: Truck {truck.id} available at Point C.")

    self.try_return()

  def tank_ready(self, tank):

    if tank.id not in self.waiting_full_tanks:
      self.waiting_full_tanks.append(tank.id)
      self.simulator.log(f"Scheduler: Tank {tank.id} ready.")

    self.try_dispatch()

  def tank_empty(self, tank):

    if tank.id not in self.waiting_empty_tanks:
        self.waiting_empty_tanks.append(tank.id)
        self.simulator.log(f"Scheduler: Tank {tank.id} empty at Point C.")

    self.try_return()

  def is_working_hours_at(self, simulation_time):
    config = self.simulator.config
    minute_of_day = (
        config.WORK_START + simulation_time
    ) % config.MINUTES_PER_DAY
    return config.WORK_START <= minute_of_day < config.WORK_END

  def next_work_start_after(self, simulation_time):
    config = self.simulator.config
    minute_of_day = (
        config.WORK_START + simulation_time
    ) % config.MINUTES_PER_DAY

    if minute_of_day < config.WORK_START:
      return simulation_time + (config.WORK_START - minute_of_day)

    if minute_of_day >= config.WORK_END:
      return (
          simulation_time
          + (config.MINUTES_PER_DAY - minute_of_day)
          + config.WORK_START
      )

    return simulation_time

  def effective_departure_time(self, target_departure):
    now = self.simulator.clock.simulation_time
    departure = max(target_departure, now)

    while not self.is_working_hours_at(departure):
      departure = self.next_work_start_after(departure)
      if departure < now:
        departure = now

    return departure

  def schedule_dispatch_ready(self, target_time):
    if self.dispatch_ready_scheduled:
      return

    departure_time = self.effective_departure_time(target_time)

    if departure_time <= self.simulator.clock.simulation_time:
      self.try_dispatch()
      return

    event = Event(
        simulation_time=departure_time,
        event_type=EventType.DISPATCH_READY,
        description="Dispatch window ready.",
    )
    self.simulator.event_queue.add_event(event)
    self.dispatch_ready_scheduled = True

  def _can_dispatch_pair(self, tank, truck):
    return (
        tank.state == TankState.READY_AT_A
        and truck.state == TruckState.IDLE_AT_A
        and truck.current_tank is None
        and tank.current_truck_head is None
    )


  def _can_return_pair(self, tank, truck):
      return (
          tank.state == TankState.EMPTY_AT_C
          and truck.state == TruckState.IDLE_AT_C
          and truck.current_tank is None
          and tank.current_truck_head is None
      )

  def try_dispatch(self):

    if not self.waiting_full_tanks:
        return

    if not self.available_trucks_at_a:
        return

    now = self.simulator.clock.simulation_time
    target_arrival = self.simulator.next_required_connection_time()

    if target_arrival is None:
      target_departure = now
    else:
      latest_arrival = self.simulator.latest_preposition_arrival_time(target_arrival)
      target_departure = latest_arrival - self.simulator.config.TRAVEL_TIME

    if target_departure > now:
      if self.can_dispatch_now():
        self.schedule_dispatch_ready(target_departure)
        return

      self.schedule_next_workday()
      return

    if not self.can_dispatch_now():
      self.schedule_next_workday()
      return

    while (
    self.waiting_full_tanks
    and self.available_trucks_at_a
    and self.can_dispatch_now()
    ):

      tank_id = self.waiting_full_tanks[0]
      truck_id = self.available_trucks_at_a[0]

      tank = self.simulator.tanks[tank_id]
      truck = self.simulator.truck_heads[truck_id]

      if not self._can_dispatch_pair(tank, truck):

          if tank.state != TankState.READY_AT_A:
              self.waiting_full_tanks.popleft()

          elif truck.state != TruckState.IDLE_AT_A:
              self.available_trucks_at_a.popleft()

          else:
              self.waiting_full_tanks.popleft()

          continue

      self.waiting_full_tanks.popleft()
      self.available_trucks_at_a.popleft()

      self.schedule_departure(tank, truck)


  def try_return(self):

    if not self.waiting_empty_tanks:
        return

    if not self.available_trucks_at_c:
        return

    if not self.can_dispatch_now():
        self.schedule_next_workday()
        return

    while (
        self.waiting_empty_tanks
        and self.available_trucks_at_c
        and self.can_dispatch_now()
    ):
      tank_id = self.waiting_empty_tanks[0]
      truck_id = self.available_trucks_at_c[0]

      tank = self.simulator.tanks[tank_id]
      truck = self.simulator.truck_heads[truck_id]

      if not self._can_return_pair(tank, truck):

          if tank.state != TankState.EMPTY_AT_C:
              self.waiting_empty_tanks.popleft()

          elif truck.state != TruckState.IDLE_AT_C:
              self.available_trucks_at_c.popleft()

          else:
              self.waiting_empty_tanks.popleft()

          continue

      self.waiting_empty_tanks.popleft()
      self.available_trucks_at_c.popleft()

      self.schedule_return(tank, truck)
  def reset(self):
    self.waiting_full_tanks.clear()
    self.waiting_empty_tanks.clear()
    self.available_trucks_at_a.clear()
    self.available_trucks_at_c.clear()

    self.workday_start_scheduled = False
    self.dispatch_ready_scheduled = False   
  def schedule_return(self, tank, truck):

    event = Event(
        simulation_time=self.simulator.clock.simulation_time,
        event_type=EventType.TRUCK_RETURN_DEPARTED,
        truck_head_id=truck.id,
        tank_id=tank.id,
        description=(
            f"Truck {truck.id} departed Point C "
            f"with empty Tank {tank.id}."
        )        
    )

    self.simulator.event_queue.add_event(event)
  def schedule_next_workday(self):

    if self.workday_start_scheduled:
        return

    next_work_start = self.simulator.clock.next_work_start_time()

    event = Event(
        simulation_time=next_work_start,
        event_type=EventType.WORKDAY_STARTED,
        description="Workday started."
    )

    self.simulator.event_queue.add_event(event)
    self.workday_start_scheduled = True