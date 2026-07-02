from enum import Enum, auto


class TankState(Enum):
    EMPTY_AT_A = auto()
    FILLING = auto()
    READY_AT_A = auto()
    IN_TRANSIT_TO_C = auto()
    WAITING_AT_C = auto()
    SUPPLYING = auto()
    EMPTY_AT_C = auto()
    IN_TRANSIT_TO_A = auto()


class Location(Enum):
    POINT_A = auto()
    POINT_B = auto()
    POINT_C = auto()


class TruckState(Enum):
    IDLE_AT_A = auto()
    DRIVING_TO_C = auto()
    IDLE_AT_C = auto()
    DRIVING_TO_A = auto()