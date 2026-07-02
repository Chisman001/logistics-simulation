from config import Config


class SimulationClock:

  def __init__(self):
    self.current_day = 1
    self.current_minute = Config.WORK_START

  def advance(self, minutes: int):
    self.current_minute += minutes

    while self.current_minute >= 1440:
      self.current_minute -= 1440
      self.current_day += 1

  def get_date_time(self):
    hours = self.current_minute // 60
    minutes = self.current_minute % 60

    return f"Day {self.current_day} - {hours:02}:{minutes:02}"