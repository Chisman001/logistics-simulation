from dataclasses import dataclass

from models.enums import TruckState, Location

@dataclass
class TruckHead:
  id: int
  state: TruckState
  location: Location
  attached_tank_id: int | None = None
  time_remaining: int = 0
  current_tank: int | None = None
  departed_at: int | None = None
  arrived_at: int | None = None
  return_started_at: int | None = None
  returned_at: int | None = None