from dataclasses import dataclass

from models.enums import TankState, Location

@dataclass
class Tank:
  id: int
  capacity: int
  state: TankState
  location: Location
  time_remaining: int = 0
  truck_head_id: int | None = None

  def __init__(self, id, capacity):
    self.id = id
    self.capacity = capacity
    self.state = TankState.IDLE_AT_A
    self.location = Location.POINT_A
    self.current_truck_head = None