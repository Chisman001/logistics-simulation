from dataclasses import dataclass

from models.enums import TruckState, Location

@dataclass
class TruckHead:
  id: int
  state: TruckState
  location: Location
  attached_tank_id: int | None = None
  time_remaining: int = 0