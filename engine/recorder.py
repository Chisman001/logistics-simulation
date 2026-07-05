import csv
from pathlib import Path


class SimulationRecorder:

    def __init__(self, filename="simulation_events.csv"):
        self.path = Path(filename)

        self.file = self.path.open(
            "w",
            newline="",
            encoding="utf-8",
        )

        self.writer = csv.writer(self.file)
        
        self.header_written = False
        
    def write_header(self, simulator):

        columns = [
            "Time",
            "Day",
            "Event",
        ]

        for truck in sorted(simulator.truck_heads.values(), key=lambda t: t.id):
            columns.append(f"Truck {truck.id}")

        for tank in sorted(simulator.tanks.values(), key=lambda t: t.id):
            columns.append(f"Tank {tank.id}")

        columns.extend([
            "Active Supply Tank",
            "Waiting Tanks At C",
            "Available Trucks At A",
            "Available Trucks At C",
        ])

        self.writer.writerow(columns)

    def close(self):
        self.file.close()
        
    def record_event(self, simulator, event):

      if not self.header_written:
          self.write_header(simulator)
          self.header_written = True

      row = [
          simulator.clock.simulation_time,
          simulator.clock.get_day(),
          event.event_type.name,
      ]

      # Record every truck
      for truck in sorted(simulator.truck_heads.values(), key=lambda t: t.id):

        tank = "-"

        if truck.current_tank is not None:
            tank = truck.current_tank

        row.append(
            f"{truck.state.name}|{truck.location.name}|Tank:{tank}"
        )

      # Record every tank
      for tank in sorted(simulator.tanks.values(), key=lambda t: t.id):

        truck = "-"

        if tank.current_truck_head is not None:
            truck = tank.current_truck_head

        row.append(
            f"{tank.state.name}|{tank.location.name}|Truck:{truck}"
        )

      # Active supply tank
      active = ""

      if simulator.active_supply_tank:
          active = simulator.active_supply_tank.id

      waiting = ",".join(
          str(t.id)
          for t in simulator.waiting_tanks_at_c
      )

      available_a = ",".join(
          str(t)
          for t in simulator.scheduler.available_trucks_at_a
      )

      available_c = ",".join(
          str(t)
          for t in simulator.scheduler.available_trucks_at_c
      )

      row.extend([
          active,
          waiting,
          available_a,
          available_c,
      ])

      self.writer.writerow(row)