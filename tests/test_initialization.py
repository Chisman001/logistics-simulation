from optimization.runner import SimulationRunner
from optimization.scenerio import Scenario
from optimization.search import Search


def test_optimizer_runs():
    search = Search()

    best, results = search.search()

    assert len(results) > 0
    assert best.score > 0

def test_runner_initializes_once():
    scenario = Scenario(
        num_tanks=4,
        num_truck_heads=2,
        tank_capacity=520,
        tank_duration=480,
        travel_time=90,
        fill_time=120,
        safety_window=60,
    )

    runner = SimulationRunner()
    simulator = runner.run(scenario)

    assert simulator.statistics.completed_deliveries >= 0
    
    fill_events = [
    e for e in simulator.event_queue.events
    if e.event_type.name == "TANK_FILL_STARTED"
    ]

    assert len(fill_events) == simulator.config.NUM_TANKS
    
    for truck in simulator.truck_heads.values():
      if truck.current_tank is not None:
          tank = simulator.tanks[truck.current_tank]
          assert tank.current_truck_head == truck.id
          
    for tank in simulator.tanks.values():
      if tank.current_truck_head is not None:
        truck = simulator.truck_heads[tank.current_truck_head]
        assert truck.current_tank == tank.id