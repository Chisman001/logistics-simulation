from dataclasses import dataclass

from models.enums import TruckState, Location

@dataclass
class TruckHead:
  id: int
  state: TruckState
  location: Location
  attached_tank_id: int | None = None
  time_remaining: int = 0

  def __init__(self, id):
    self.id = id
    self.state = TruckState.IDLE_AT_A
    self.location = Location.POINT_A
    self.current_tank = None