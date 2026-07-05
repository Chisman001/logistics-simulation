import csv


class EventExporter:

    def __init__(self):
        self.filename = "simulation_events.csv"

    def export(self, events):
        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Time",
                "Day",
                "Event",
                "Truck",
                "Tank",
                "Truck State",
                "Tank State",
                "Truck Location",
                "Tank Location",
            ])

            writer.writerows(events)