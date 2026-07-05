
class Config:
  # Tank
  TANK_CAPACITY = 520
  TANK_DURATION = 8 * 60      # minutes

  # Filling
  FILL_TIME = 2 * 60

  # Travel
  TRAVEL_TIME = 90

  # Safety
  SAFETY_WINDOW = 60

  # Working hours
  WORK_START = 6 * 60
  WORK_END = 18 * 60

  # Resources   
  NUM_TANKS = 4
  NUM_TRUCK_HEADS = 2

  # Simulation
  SIMULATION_DAYS = 30
  DEBUG_HANDOVER = False
  PRINT_SUPPLY_TIMELINE = False
  VALIDATE_ON_COMPLETE = True

  # Time
  MINUTES_PER_DAY = 24 * 60
  
  # Reporting
  PRINT_REPORTS = True
  PRINT_EVENTS = True