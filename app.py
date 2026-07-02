
from engine.simulation import Simulator

simulator = Simulator()

simulator.initialize()

print(simulator.clock.get_date_time())

print()

print("Tanks")
for tank in simulator.tanks:
    print(tank)

print()

print("Truck Heads")
for truck in simulator.truck_heads:
    print(truck)

