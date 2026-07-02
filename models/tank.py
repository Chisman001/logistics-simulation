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