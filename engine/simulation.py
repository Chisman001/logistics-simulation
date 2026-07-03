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
    self.config = Config
    self.scheduler = Scheduler(self)

    self.clock = SimulationClock()

    self.tanks = {}

    self.truck_heads = {}

    self.event_queue = EventQueue()

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
    self.create_tanks()
    self.create_truck_heads()
    self.scheduler.schedule_initial_events()
    print("Initializing simulation...")
    print(f"Created {len(self.tanks)} tanks.")
    print(f"Created {len(self.truck_heads)} truck heads.")
    print("Simulation ready.")

  def process_event(self, event):
    self.clock.simulation_time = event.simulation_time

    print(
      f"[{self.clock.get_date_time()}] "
      f"{event.event_type.name}: "
      f"{event.description}"
    )

    if event.event_type == EventType.TANK_FILL_STARTED:
      self.handle_tank_fill_started(event)

    elif event.event_type == EventType.TANK_FILL_COMPLETED:
      self.handle_tank_fill_completed(event)

    elif event.event_type == EventType.TRUCK_DEPARTED:
      self.handle_truck_departed(event)

    elif event.event_type == EventType.TRUCK_ARRIVED:
      self.handle_truck_arrived(event)
  def run(self):
    while not self.event_queue.is_empty():

      event = self.event_queue.get_next_event()

      self.process_event(event)

  def handle_tank_fill_started(self, event):
    tank = self.tanks[event.resource_id]

    tank.state = TankState.FILLING

    print(f"Tank {tank.id} is now filling.")

    completion_event = Event(
        simulation_time=event.simulation_time + self.config.FILL_TIME,
        event_type=EventType.TANK_FILL_COMPLETED,
        resource_id=tank.id,
        description=f"Tank {tank.id} finished filling."
    )

    self.event_queue.add_event(completion_event)


  def handle_tank_fill_completed(self, event):
    tank = self.tanks[event.resource_id]
    tank.state = TankState.READY_AT_A
    self.scheduler.on_tank_ready(tank)


  def handle_truck_departed(self, event):
    print("Handling truck departure...")


  def handle_truck_arrived(self, event):
    print("Handling truck arrival...")

  def get_available_trucks(self):

    return [
        truck
        for truck in self.truck_heads.values()
        if truck.state == TruckState.IDLE_AT_A
    ]