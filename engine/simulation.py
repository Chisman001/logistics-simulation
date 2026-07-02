from config import Config
from engine.clock import SimulationClock
from models.tank import Tank
from models.enums import TankState, Location
from models.truck_head import TruckHead
from models.enums import TruckState
from engine.scheduler import Scheduler


class Simulator:
  def __init__(self):
    self.config = Config
    self.scheduler = Scheduler(self)

    self.clock = SimulationClock()

    self.tanks = []

    self.truck_heads = []

    self.event_queue = []

  def create_tanks(self):
    for i in range(1, self.config.NUM_TANKS + 1):
      tank = Tank(
        id=i,
        capacity=self.config.TANK_CAPACITY,
        state=TankState.EMPTY_AT_A,
        location=Location.POINT_A,
      )

      self.tanks.append(tank)

  def create_truck_heads(self):
    for i in range(1, self.config.NUM_TRUCK_HEADS + 1):
      truck_head = TruckHead(
        id=i,
        state=TruckState.IDLE_AT_A,
        location=Location.POINT_A,
      )

      self.truck_heads.append(truck_head)

  def initialize(self):
    self.create_tanks()
    self.create_truck_heads()
    print("Initializing simulation...")
    print(f"Created {len(self.tanks)} tanks.")
    print(f"Created {len(self.truck_heads)} truck heads.")
    print("Simulation ready.")