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
  current_truck_head: int | None = None
  fill_started_at: int | None = None
  fill_completed_at: int | None = None
  supply_started_at: int | None = None
  empty_at: int | None = None
  return_started_at: int | None = None
  returned_at: int | None = None
  departed_at: int | None = None
  arrived_at: int | None = None