from engine.event import Event
from config import Config
from engine.clock import SimulationClock
from engine.event_queue import EventQueue
from models.tank import Tank
from models.enums import TankState, Location, EventType
from models.truck_head import TruckHead
from models.enums import TruckState
from engine.scheduler import Scheduler


class Simulator:
  def __init__(self):
    self.config = Config()
    self.scheduler = Scheduler(self)

    self.clock = SimulationClock()

    self.tanks = {}

    self.truck_heads = {}

    self.event_queue = EventQueue()
    self.last_log_day = None
    self.last_log_time = None

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
    print("Initializing simulation...")
    self.create_tanks()
    self.create_truck_heads()
    print(f"Created {len(self.tanks)} tanks.")
    print(f"Created {len(self.truck_heads)} truck heads.")
    print("Simulation ready.")
    for truck in self.truck_heads.values():
      self.scheduler.truck_available_at_a(truck)
    self.scheduler.schedule_initial_events()

  def log(self, message):
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

    elif event.event_type == EventType.TANK_EMPTY:
      self.handle_tank_empty(event)
    elif event.event_type == EventType.TRUCK_RETURN_DEPARTED:
      self.handle_truck_return_departed(event)

    elif event.event_type == EventType.TRUCK_RETURN_ARRIVED:
      self.handle_truck_return_arrived(event)

    elif event.event_type == EventType.WORKDAY_STARTED:
      self.handle_workday_started(event)

    self.assert_consistent_state()
  def run(self):
    end_time = (
      self.config.SIMULATION_DAYS * self.config.MINUTES_PER_DAY
      - self.config.WORK_START
    )

    while not self.event_queue.is_empty():

      event = self.event_queue.get_next_event()

      if event.simulation_time >= end_time:
        break

      self.process_event(event)

  def handle_tank_fill_started(self, event):
    tank = self.tanks[event.tank_id]

    tank.state = TankState.FILLING

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
    tank.state = TankState.READY_AT_A
    self.scheduler.tank_ready(tank)


  def handle_truck_departed(self, event):

    truck = self.truck_heads[event.truck_head_id]
    tank = self.tanks[event.tank_id]

    truck.state = TruckState.DRIVING_TO_C
    truck.location = Location.IN_TRANSIT_TO_C

    tank.state = TankState.IN_TRANSIT_TO_C
    tank.location = Location.IN_TRANSIT_TO_C

    truck.current_tank = tank.id
    tank.current_truck_head = truck.id

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

    # Get truck
    truck = self.truck_heads[event.truck_head_id]

    # Get tank
    tank = self.tanks[event.tank_id]

    # Move both to Point C
    truck.location = Location.POINT_C
    tank.location = Location.POINT_C

    # Disconnect truck from tank
    truck.current_tank = None
    tank.current_truck_head = None

    # Truck becomes available at Point C
    truck.state = TruckState.IDLE_AT_C

    # Tank begins supplying
    tank.state = TankState.SUPPLYING

    # Schedule TANK_EMPTY event
    empty_event = Event(
        simulation_time=(
            event.simulation_time
            + self.config.TANK_DURATION
        ),
        event_type=EventType.TANK_EMPTY,
        truck_head_id=None,
        tank_id=tank.id,
        description=f"Tank {tank.id} is now empty."
    )
    self.event_queue.add_event(empty_event)
    self.scheduler.truck_available_at_c(truck)

  def handle_tank_empty(self, event):
    tank = self.tanks[event.tank_id]

    tank.state = TankState.EMPTY_AT_C
    tank.location = Location.POINT_C

    self.scheduler.tank_empty(tank)

  def handle_truck_return_departed(self, event):

    truck = self.truck_heads[event.truck_head_id]
    tank = self.tanks[event.tank_id]

    truck.state = TruckState.DRIVING_TO_A
    truck.location = Location.IN_TRANSIT_TO_A

    tank.state = TankState.IN_TRANSIT_TO_A
    tank.location = Location.IN_TRANSIT_TO_A

    truck.current_tank = tank.id
    tank.current_truck_head = truck.id

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
        f"Truck {truck.id} and Tank {tank.id} disagree about their link."
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
