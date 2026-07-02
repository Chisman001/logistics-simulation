from config import Config


class SimulationClock:

  def __init__(self):
    self.current_day = 1
    self.current_minute = Config.WORK_START