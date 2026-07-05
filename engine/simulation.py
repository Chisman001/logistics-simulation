from analytics.metrics import Metrics
from analytics.reports import Report
from analytics.validator import SimulationValidator
from engine.event import Event
from config import Config
from engine.clock import SimulationClock
from engine.event_queue import EventQueue
from models.tank import Tank
from models.enums import TankState, Location, EventType
from models.truck_head import TruckHead
from models.enums import TruckState
from engine.scheduler import Scheduler
from analytics.statistics import Statistics


class Simulator:
  def __init__(self, config=None):
    if config is None:
      config = Config()
    self.config = config
    self.statistics = Statistics()
    self.scheduler = Scheduler(self)

    self.clock = SimulationClock()

    self.tanks = {}

    self.truck_heads = {}

    self.event_queue = EventQueue()
    self.last_log_day = None
    self.last_log_time = None
    self.active_supply_tank = None
    self.waiting_tanks_at_c = []
    self.pending_supply_tank = None
    self.supply_gap_started_at = None

  def create_tanks(self):
    self.tanks = {}

    for i in range(1, self.config.NUM_TANKS + 1):
      tank = Tank(
        id=i,
        capacity=self.config.TANK_CAPACITY,
        state=TankState.EMPTY_AT_A,
        location=Location.POINT_A,
      )

      self.tanks[i] = tank

  def create_truck_heads(self):
    for i in range(1, self.config.NUM_TRUCK_HEADS + 1):
      truck_head = TruckHead(
        id=i,
        state=TruckState.IDLE_AT_A,
        location=Location.POINT_A,
      )

      self.truck_heads[i] = truck_head

  def initialize(self):
    self.statistics = Statistics()
    self.event_queue = EventQueue()

    self.active_supply_tank = None
    self.waiting_tanks_at_c = []
    self.pending_supply_tank = None
    self.supply_gap_started_at = None

    self.scheduler.reset()
    if self.config.PRINT_EVENTS:
        print("Initializing simulation...")

    self.create_tanks()
    self.create_truck_heads()

    if self.config.PRINT_EVENTS:
        print(f"Created {len(self.tanks)} tanks.")
        print(f"Created {len(self.truck_heads)} truck heads.")
        print("Simulation ready.")

    for truck in self.truck_heads.values():
        self.scheduler.truck_available_at_a(truck)

    self.scheduler.schedule_initial_events()

  def log(self, message):
    if not self.config.PRINT_EVENTS:
        return

    day = self.clock.get_day()
    time = self.clock.get_time()

    if day != self.last_log_day:
        print()
        print(f"========== Day {day} ==========")
        self.last_log_day = day
        self.last_log_time = None

    if time != self.last_log_time:
        print()
        print(time)
        self.last_log_time = time

    print(f"    {message}")

  def process_event(self, event):
    print(
      f"Processing {event.event_type.name} "
      f"Truck={event.truck_head_id} "
      f"Tank={event.tank_id} "
      f"Time={event.simulation_time}"
    )
    self.clock.simulation_time = event.simulation_time

    self.log(event.description)

    if event.event_type == EventType.TANK_FILL_STARTED:
      self.handle_tank_fill_started(event)

    elif event.event_type == EventType.TANK_FILL_COMPLETED:
      self.handle_tank_fill_completed(event)

    elif event.event_type == EventType.TRUCK_DEPARTED:
      self.handle_truck_departed(event)

    elif event.event_type == EventType.TRUCK_ARRIVED:
      self.handle_truck_arrived(event)

    elif event.event_type == EventType.SUPPLY_STARTED:
      self.handle_supply_started(event)

    elif event.event_type == EventType.TANK_EMPTY:
      self.handle_tank_empty(event)
    elif event.event_type == EventType.TRUCK_RETURN_DEPARTED:
      self.handle_truck_return_departed(event)

    elif event.event_type == EventType.TRUCK_RETURN_ARRIVED:
      self.handle_truck_return_arrived(event)

    elif event.event_type == EventType.WORKDAY_STARTED:
      self.handle_workday_started(event)

    elif event.event_type == EventType.DISPATCH_READY:
      self.handle_dispatch_ready(event)
    for truck in self.truck_heads.values():
      print(
        f"Truck {truck.id}: "
        f"state={truck.state.name}, "
        f"tank={truck.current_tank}"
      )

    for tank in self.tanks.values():
      print(
        f"Tank {tank.id}: "
        f"state={tank.state.name}, "
        f"truck={tank.current_truck_head}"
      )
    self.assert_consistent_state()
  def run(self):
    self.initialize()
    print("Events in queue:", len(self.event_queue.events))
    end_time = (
      self.config.SIMULATION_DAYS * self.config.MINUTES_PER_DAY
      - self.config.WORK_START
    )

    while not self.event_queue.is_empty():

      event = self.event_queue.get_next_event()

      if event.simulation_time >= end_time:
        break

      self.process_event(event)

    self.statistics.simulation_duration = self.clock.simulation_time
    metrics = Metrics(self.statistics)

    validation_result = None
    if self.config.VALIDATE_ON_COMPLETE:
      validator = SimulationValidator(self.statistics, self.config)
      validation_result = validator.validate()
    if self.config.PRINT_REPORTS:
        validator.print_report()

        if (
            self.config.PRINT_SUPPLY_TIMELINE
            or self.config.SIMULATION_DAYS <= 2
        ):
            validator.print_supply_timeline()

    report = Report(metrics, self.config, validation_result)

    if self.config.PRINT_REPORTS:
      report.print_summary()
      report.print_baseline_report()

  def handle_tank_fill_started(self, event):
    tank = self.tanks[event.tank_id]
    # Ignore stale or duplicate fill-start events
    if tank.state not in (
        TankState.EMPTY_AT_A,
        TankState.FILLING,
    ):
        return

    tank.state = TankState.FILLING
    tank.fill_started_at = event.simulation_time
    self.statistics.record_fill()

    self.log(f"Tank {tank.id} is now filling.")

    completion_event = Event(
        simulation_time=event.simulation_time + self.config.FILL_TIME,
        event_type=EventType.TANK_FILL_COMPLETED,
        tank_id=tank.id,
        description=f"Tank {tank.id} finished filling."
    )

    self.event_queue.add_event(completion_event)


  def handle_tank_fill_completed(self, event):
    tank = self.tanks[event.tank_id]
    # Ignore duplicate or stale completion events
    if tank.state != TankState.FILLING:
        return
    tank.state = TankState.READY_AT_A
    tank.fill_completed_at = event.simulation_time
    self.scheduler.tank_ready(tank)
    self.preposition_ready_tanks_for_next_handover()

  def preposition_ready_tanks_for_next_handover(self):
    if self.active_supply_tank is None:
      return

    target_arrival = self.next_required_connection_time()
    if target_arrival is None:
      return

    for tank in list(self.tanks.values()):
      if tank.state != TankState.READY_AT_A:
        continue

      if tank.supply_started_at is not None:
        continue

      if tank.id in self.scheduler.waiting_full_tanks:
        self.scheduler.waiting_full_tanks.remove(tank.id)

      tank.state = TankState.WAITING_AT_C
      tank.location = Location.POINT_C
      tank.arrived_at = self.clock.simulation_time

      if tank not in self.waiting_tanks_at_c:
        self.waiting_tanks_at_c.append(tank)

      self.log(f"Tank {tank.id} pre-positioned at Point C for the next handover.")

    self.promote_next_waiting_tank()

  def handle_truck_departed(self, event):

    truck = self.truck_heads[event.truck_head_id]
    tank = self.tanks[event.tank_id]

    truck.state = TruckState.DRIVING_TO_C
    truck.location = Location.IN_TRANSIT_TO_C

    tank.state = TankState.IN_TRANSIT_TO_C
    tank.location = Location.IN_TRANSIT_TO_C

    truck.current_tank = tank.id
    tank.current_truck_head = truck.id

    # Record departure timestamps
    truck.departed_at = event.simulation_time
    tank.departed_at = event.simulation_time
    tank.arrived_at = None
    tank.supply_started_at = None
    tank.empty_at = None
    self.statistics.record_dispatch()
    self.statistics.record_truck_movement(
        truck.id, "TRUCK_DEPARTED", event.simulation_time, tank.id
    )
    if tank.fill_completed_at is not None:
      waiting = tank.departed_at - tank.fill_completed_at
      self.statistics.record_tank_wait(waiting)

    arrival = Event(
    simulation_time=(
        event.simulation_time
        + self.config.TRAVEL_TIME
    ),

    event_type=EventType.TRUCK_ARRIVED,

    truck_head_id=truck.id,
    tank_id=tank.id,

    description=(
        f"Truck {truck.id} arrived "
        f"with Tank {tank.id}."
    )
    )

    self.event_queue.add_event(arrival)


  def handle_truck_arrived(self, event):

    truck = self.truck_heads[event.truck_head_id]
    tank = self.tanks[event.tank_id]

    truck.location = Location.POINT_C
    tank.location = Location.POINT_C

    truck.current_tank = None
    tank.current_truck_head = None

    truck.state = TruckState.IDLE_AT_C
    tank.state = TankState.WAITING_AT_C

    truck.arrived_at = event.simulation_time
    tank.arrived_at = event.simulation_time

    if tank not in self.waiting_tanks_at_c:
      self.waiting_tanks_at_c.append(tank)

    self.scheduler.truck_available_at_c(truck)
    self.promote_next_waiting_tank()

  def next_required_connection_time(self):
    if self.active_supply_tank is None:
      return None

    return (
        self.active_supply_tank.supply_started_at
        + self.config.TANK_DURATION
        - self.config.SAFETY_WINDOW
    )

  def latest_preposition_arrival_time(self, target_arrival):
    if target_arrival is None:
      return None

    day_start = self.clock.simulation_time - (self.clock.simulation_time % self.config.MINUTES_PER_DAY)
    work_end = day_start + self.config.WORK_END
    return min(target_arrival, work_end)

  def has_successor_at_c(self):
    for tank in self.tanks.values():
      if tank.state == TankState.IN_TRANSIT_TO_C:
        return True

    return False

  def _consumer_has_supply(self):
    for tank in self.tanks.values():
      if tank.state == TankState.SUPPLYING:
        return True

    if self.pending_supply_tank is not None:
      return True

    return False

  def _record_supply_gap_downtime(self, resume_time):
    if self.supply_gap_started_at is None:
      return

    gap = resume_time - self.supply_gap_started_at
    if gap > 0:
      self.statistics.record_customer_downtime(gap)
    self.supply_gap_started_at = None

  def log_handover_trace(
    self,
    tank,
    arrival_time,
    supply_start,
    expected_empty,
    required_connection,
    delay,
    downtime,
  ):
    print()
    print(f"Tank {tank.id}")
    print(f"  Arrived:           {arrival_time}")
    print(f"  Supply starts:     {supply_start}")
    print(f"  Expected empty:    {expected_empty}")
    print(f"  Required connect:  {required_connection}")
    print(f"  Wait at C:         {supply_start - arrival_time}")
    print(f"  Safety delay:      {delay}")
    print(f"  Downtime:          {downtime}")

  def schedule_supply_start(self, tank, arrival_time):
    if tank.supply_started_at is not None:
      return

    if self.pending_supply_tank is not None:
      return

    previous = self.active_supply_tank
    expected_empty = None
    required_connection = None
    delay = 0
    downtime = 0

    if previous is None:
      if self.clock.simulation_time == 0:
        supply_start = self.config.WORK_START
      else:
        supply_start = max(arrival_time, self.clock.simulation_time)
    else:
      expected_empty = (
          previous.supply_started_at + self.config.TANK_DURATION
      )
      required_connection = expected_empty - self.config.SAFETY_WINDOW
      supply_start = max(arrival_time, required_connection)
      if supply_start < self.clock.simulation_time:
        supply_start = self.clock.simulation_time

      if supply_start > expected_empty:
        downtime = supply_start - expected_empty
        self.statistics.record_customer_downtime(downtime)

      if supply_start > required_connection:
        delay = supply_start - required_connection
        self.statistics.record_safety_violation(delay)

    if self.config.DEBUG_HANDOVER:
      self.log_handover_trace(
          tank,
          arrival_time,
          supply_start,
          expected_empty,
          required_connection,
          delay,
          downtime,
      )

    if supply_start <= self.clock.simulation_time:
      self.start_supply_for_tank(tank, self.clock.simulation_time)
    else:
      self.schedule_supply_changeover(tank, supply_start)

    if self.active_supply_tank is None and self.pending_supply_tank is None:
      self.preposition_ready_tanks_for_next_handover()

    if self.active_supply_tank is None and self.pending_supply_tank is None:
      self.preposition_ready_tanks_for_next_handover()

  def promote_next_waiting_tank(self):
    if not self.waiting_tanks_at_c:
      return

    if self.pending_supply_tank is not None:
      return

    next_tank = self.waiting_tanks_at_c[0]

    if next_tank.state != TankState.WAITING_AT_C:
      return

    if next_tank.supply_started_at is not None:
      return

    if next_tank.arrived_at is None:
      return

    self.schedule_supply_start(next_tank, next_tank.arrived_at)

  def schedule_supply_changeover(self, tank, start_time):
    if tank.supply_started_at is not None:
      return

    if self.pending_supply_tank is not None:
      return

    self.pending_supply_tank = tank
    changeover_event = Event(
        simulation_time=start_time,
        event_type=EventType.SUPPLY_STARTED,
        truck_head_id=None,
        tank_id=tank.id,
        description=f"Tank {tank.id} started supplying."
    )
    self.event_queue.add_event(changeover_event)

  def start_supply_for_tank(self, tank, event_time):
    if tank.supply_started_at is not None:
      return

    if tank.state != TankState.WAITING_AT_C:
      return

    if tank in self.waiting_tanks_at_c:
      self.waiting_tanks_at_c.remove(tank)

    self.active_supply_tank = tank

    tank.state = TankState.SUPPLYING
    tank.supply_started_at = event_time
    self.statistics.record_supply()
    self.statistics.open_supply_interval(
        tank.id, event_time, tank.arrived_at
    )
    self._record_supply_gap_downtime(event_time)
    self.pending_supply_tank = None
    self.preposition_ready_tanks_for_next_handover()

    self.log(f"Tank {tank.id} started supplying.")

    empty_event = Event(
        simulation_time=(event_time + self.config.TANK_DURATION),
        event_type=EventType.TANK_EMPTY,
        truck_head_id=None,
        tank_id=tank.id,
        description=f"Tank {tank.id} is now empty."
    )
    self.event_queue.add_event(empty_event)
    self.promote_next_waiting_tank()
    self.scheduler.try_dispatch()

  def handle_supply_started(self, event):
    tank = self.tanks[event.tank_id]

    if tank.supply_started_at is not None:
      return

    if tank.state != TankState.WAITING_AT_C:
      return

    self.start_supply_for_tank(tank, event.simulation_time)

  def handle_tank_empty(self, event):
    tank = self.tanks[event.tank_id]

    tank.empty_at = event.simulation_time
    self.statistics.close_supply_interval(tank.id, event.simulation_time)
    self.statistics.record_delivery(tank)

    tank.state = TankState.EMPTY_AT_C
    tank.location = Location.POINT_C

    self.scheduler.tank_empty(tank)

    if self.active_supply_tank is tank:
      self.active_supply_tank = None
      self.promote_next_waiting_tank()

    if not self._consumer_has_supply() and self.supply_gap_started_at is None:
      self.supply_gap_started_at = event.simulation_time

    self.scheduler.try_dispatch()

  def handle_dispatch_ready(self, event):
    self.scheduler.dispatch_ready_scheduled = False
    self.scheduler.try_dispatch()

  def handle_truck_return_departed(self, event):

    truck = self.truck_heads[event.truck_head_id]
    tank = self.tanks[event.tank_id]

    truck.state = TruckState.DRIVING_TO_A
    truck.location = Location.IN_TRANSIT_TO_A

    tank.state = TankState.IN_TRANSIT_TO_A
    tank.location = Location.IN_TRANSIT_TO_A

    truck.current_tank = tank.id
    tank.current_truck_head = truck.id

    # Record return departure timestamps
    truck.return_departed_at = event.simulation_time
    truck.return_started_at = event.simulation_time
    tank.return_departed_at = event.simulation_time
    tank.return_started_at = event.simulation_time

    if tank.empty_at is not None:
      waiting_time = tank.return_departed_at - tank.empty_at
      self.statistics.record_empty_wait(waiting_time)

    self.statistics.record_truck_movement(
        truck.id, "TRUCK_RETURN_DEPARTED", event.simulation_time, tank.id
    )

    arrival = Event(
    simulation_time=(
        event.simulation_time
        + self.config.TRAVEL_TIME
    ),

    event_type=EventType.TRUCK_RETURN_ARRIVED,

    truck_head_id=truck.id,
    tank_id=tank.id,

    description=(
        f"Truck {truck.id} returned "
        f"Tank {tank.id} to Point A."
    )
    )

    self.event_queue.add_event(arrival)

  def handle_truck_return_arrived(self, event):
    # when truck reaches point A
    truck = self.truck_heads[event.truck_head_id]
    tank = self.tanks[event.tank_id]

    # Update truck state and location
    truck.state = TruckState.IDLE_AT_A
    truck.location = Location.POINT_A

    # Update tank state and location
    tank.state = TankState.EMPTY_AT_A
    tank.location = Location.POINT_A

    # Disconnect truck from tank
    truck.current_tank = None
    tank.current_truck_head = None

    # Record return completion timestamps
    truck.return_arrived_at = event.simulation_time
    truck.returned_at = event.simulation_time
    tank.returned_at = event.simulation_time
    tank.total_cycles += 1
    truck.total_trips += 1

    self.statistics.record_cycle(tank)
    self.statistics.record_return()

    # Notify scheduler that truck is available at Point A
    self.scheduler.truck_available_at_a(truck)

    # start filling returned tank
    fill_event = Event(
        simulation_time=event.simulation_time,
        event_type=EventType.TANK_FILL_STARTED,
        tank_id=tank.id,
        description=f"Tank {tank.id} started filling."
    )
    self.event_queue.add_event(fill_event)

  def handle_workday_started(self, event):

    self.scheduler.workday_start_scheduled = False

    self.scheduler.try_dispatch()

    self.scheduler.try_return()

  def assert_consistent_state(self):
    expected_truck_locations = {
      TruckState.IDLE_AT_A: Location.POINT_A,
      TruckState.DRIVING_TO_C: Location.IN_TRANSIT_TO_C,
      TruckState.IDLE_AT_C: Location.POINT_C,
      TruckState.DRIVING_TO_A: Location.IN_TRANSIT_TO_A,
    }

    expected_tank_locations = {
      TankState.EMPTY_AT_A: Location.POINT_A,
      TankState.FILLING: Location.POINT_A,
      TankState.READY_AT_A: Location.POINT_A,
      TankState.IN_TRANSIT_TO_C: Location.IN_TRANSIT_TO_C,
      TankState.WAITING_AT_C: Location.POINT_C,
      TankState.SUPPLYING: Location.POINT_C,
      TankState.EMPTY_AT_C: Location.POINT_C,
      TankState.IN_TRANSIT_TO_A: Location.IN_TRANSIT_TO_A,
    }

    for truck in self.truck_heads.values():
      assert truck.location == expected_truck_locations[truck.state], (
        f"Truck {truck.id} state {truck.state.name} does not match "
        f"location {truck.location.name}."
      )

      if truck.current_tank is None:
        continue

      assert truck.current_tank in self.tanks, (
        f"Truck {truck.id} references missing Tank {truck.current_tank}."
      )

      tank = self.tanks[truck.current_tank]
      assert tank.current_truck_head == truck.id, (
        f"""
      Truck {truck.id} thinks it has Tank {truck.current_tank}
      Tank {tank.id} thinks it is on Truck {tank.current_truck_head}

      Truck state: {truck.state}
      Tank state: {tank.state}
      Truck location: {truck.location}
      Tank location: {tank.location}
      """
      )

    for tank in self.tanks.values():
      assert tank.location == expected_tank_locations[tank.state], (
        f"Tank {tank.id} state {tank.state.name} does not match "
        f"location {tank.location.name}."
      )

      if tank.current_truck_head is None:
        continue

      assert tank.current_truck_head in self.truck_heads, (
        f"Tank {tank.id} references missing Truck {tank.current_truck_head}."
      )

      truck = self.truck_heads[tank.current_truck_head]
      assert truck.current_tank == tank.id, (
        f"Tank {tank.id} and Truck {truck.id} disagree about their link."
      )
