from dataclasses import dataclass, field

from models.enums import EventType

@dataclass(order=True)
class Event:
  simulation_time: int
  sequence: int = field(default=0, init=False)
  event_type: EventType = field(compare=False)
  truck_head_id: int | None = field(default=None, compare=False)
  tank_id: int | None = field(default=None, compare=False)
  description: str = field(default="", compare=False)
