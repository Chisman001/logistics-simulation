from engine.simulation import Simulator
from optimization.optimizer import Optimizer
from optimization.scenerio import Scenario

def main():
    simulator = Simulator()
    simulator.initialize()
    simulator.run()

if __name__ == "__main__":
    main()




scenario = Scenario(
    num_tanks=4,
    num_truck_heads=2,
    tank_capacity=520,
    tank_duration=480,
    travel_time=90,
    fill_time=120,
    safety_window=60,
)

optimizer = Optimizer()

result = optimizer.evaluate(scenario)

print()
print("=" * 40)
print("Optimizer Test")
print("=" * 40)

print(f"Score: {result.score}")
print(f"Deliveries: {result.statistics.completed_deliveries}")
print(f"Downtime: {result.statistics.total_consumer_downtime}")
print(f"Safety Violations: {result.statistics.safety_violations}")