from dataclasses import dataclass

from models.enums import EventType

@dataclass(order=True)
class Event:
  simulation_time: int
  event_type: EventType
  truck_head_id: int | None = None
  tank_id: int | None = None
  description: str = ""