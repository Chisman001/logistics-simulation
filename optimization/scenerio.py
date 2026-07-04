from dataclasses import dataclass


@dataclass
class Scenario:
  num_tanks: int
  num_truck_heads: int
  tank_capacity: int
  tank_duration: int
  travel_time: int
  fill_time: int
  safety_window: int

Scenario(
  num_tanks=4,
  num_truck_heads=2,
  tank_capacity=520,
  tank_duration=480,
  travel_time=90,
  fill_time=120,
  safety_window=60,
)