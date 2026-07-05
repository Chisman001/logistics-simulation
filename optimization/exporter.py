import csv
from pathlib import Path


class OptimizationExporter:

    def export(
        self,
        results,
        filename="optimization_results.csv",
    ):

        path = Path(filename)

        with path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)

            self._write_header(writer)

            for result in results:
                self._write_result(writer, result)

        return path
      
    def _write_header(self, writer):

      writer.writerow([
        "Score",

        "Tanks",
        "Truck Heads",
        "Tank Capacity",
        "Tank Duration",

        "Travel Time",
        "Fill Time",
        "Safety Window",

        "Deliveries",
        "Dispatches",
        "Returns",

        "Downtime",
        "Safety Violations",

        "Average Tank Wait",
        "Average Cycle Time",
        "Average Delivery Time",
        "Average Empty Tank Wait",
      ])
      
    def _write_result(
    self,
    writer,
    result,
    ):

        scenario = result.scenario

        summary = result.metrics.simulation_summary()

        tank = result.metrics.tank_performance()

        fleet = result.metrics.fleet_performance()

        safety = result.metrics.safety_metrics()

        consumer = result.metrics.consumer_service()

        writer.writerow([

            result.score,

            scenario.num_tanks,
            scenario.num_truck_heads,
            scenario.tank_capacity,
            scenario.tank_duration,

            scenario.travel_time,
            scenario.fill_time,
            scenario.safety_window,

            summary["Completed Deliveries"],
            summary["Dispatches"],
            summary["Returns"],

            consumer["Consumer Downtime (reported)"],

            safety["Safety Violations"],

            tank["Average Tank Wait"],
            tank["Average Cycle Time"],
            tank["Average Delivery Time"],

            fleet["Average Empty Tank Wait"],
        ])