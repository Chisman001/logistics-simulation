from dataclasses import dataclass

from models.enums import EventType

@dataclass(order=True)
class Event:
  time: int
  event_type: EventType
  description: str