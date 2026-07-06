import json
class Config:
  def __init__(self):

        with open("config.json") as file:

            settings = json.load(file)

        self.NUM_TRUCK_HEADS = settings["trucks"]

        self.NUM_TANKS = settings["tanks"]

        self.SIMULATION_DAYS = settings["days"]
        # Tank
        self.TANK_CAPACITY = 520
        self.TANK_DURATION = 8 * 60      # minutes

        # Filling
        self.FILL_TIME = 2 * 60

        # Travel
        self.TRAVEL_TIME = 90

        # Safety
        self.SAFETY_WINDOW = 60

        # Working hours
        self.WORK_START = 6 * 60
        self.WORK_END = 18 * 60

        # Simulation
        self.DEBUG_HANDOVER = False
        self.PRINT_SUPPLY_TIMELINE = False
        self.VALIDATE_ON_COMPLETE = True

        # Time
        self.MINUTES_PER_DAY = 24 * 60
        
        # Reporting
        self.PRINT_REPORTS = True
        self.PRINT_EVENTS = True