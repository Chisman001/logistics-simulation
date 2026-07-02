from models.tank import Tank
from models.enums import TankState, Location
from models.truck_head import TruckHead
from models.enums import TruckState, Location
from engine.clock import SimulationClock

clock = SimulationClock()

print(clock.current_day)
print(clock.current_minute)

truck = TruckHead(
    id=1,
    state=TruckState.IDLE_AT_A,
    location=Location.POINT_A
)

print(truck)

tank = Tank(
    id=1,
    capacity=520,
    state=TankState.EMPTY_AT_A,
    location=Location.POINT_A
)

print(tank)