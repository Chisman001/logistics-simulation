from engine.event import Event
from engine.event_queue import EventQueue
from models.enums import EventType

queue = EventQueue()

queue.add_event(
    Event(
        time=450,
        event_type=EventType.TRUCK_ARRIVED,
        resource_id=1,
        description="Truck arrived."
    )
)

queue.add_event(
    Event(
        time=360,
        event_type=EventType.TANK_FILL_STARTED,
        resource_id=1,
        description="Tank filling started."
    )
)

queue.add_event(
    Event(
        time=600,
        event_type=EventType.TANK_EMPTY,
        resource_id=1,
        description="Tank became empty."
    )
)

while not queue.is_empty():
    print(queue.get_next_event())