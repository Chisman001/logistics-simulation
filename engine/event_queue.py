import heapq

from engine.event import Event

class EventQueue:
    def __init__(self):
        self.events = []

    def add_event(self, event: Event):
        heapq.heappush(self.events, event)

    def get_next_event(self) -> Event:
        if self.events:
            return heapq.heappop(self.events)
        else:
            return None

    def is_empty(self) -> bool:
        return len(self.events) == 0
    
    def size(self) -> int:
        return len(self.events)