from config import Config


class SimulationClock:

  def __init__(self):
    self.simulation_time = 0

  def advance(self, minutes: int):
    self.simulation_time += minutes

  def get_day(self):
    return (self.simulation_time // Config.MINUTES_PER_DAY) + 1

  def get_time(self):
    minutes_since_day_start = self.simulation_time % Config.MINUTES_PER_DAY

    total_minutes = Config.WORK_START + minutes_since_day_start

    total_minutes %= Config.MINUTES_PER_DAY

    hours = total_minutes // 60
    minutes = total_minutes % 60

    return f"{hours:02}:{minutes:02}"

  def get_date_time(self):
    return f"Day {self.get_day()} - {self.get_time()}"