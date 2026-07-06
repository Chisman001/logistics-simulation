from config import Config

class SimulationClock:

  def __init__(self, config):
    self.simulation_time = 0
    self.config = config

  def advance(self, minutes: int):
    self.simulation_time += minutes

  def get_day(self):
    total_minutes = self.config.WORK_START + self.simulation_time

    return (total_minutes // self.config.MINUTES_PER_DAY) + 1

  def get_time(self):
    minutes_since_day_start = self.simulation_time % self.config.MINUTES_PER_DAY

    total_minutes = self.config.WORK_START + minutes_since_day_start

    total_minutes %= self.config.MINUTES_PER_DAY

    hours = total_minutes // 60
    minutes = total_minutes % 60

    return f"{hours:02}:{minutes:02}"

  def get_date_time(self):
    return f"Day {self.get_day()} - {self.get_time()}"

  def current_minute_of_day(self):
    total = (
        self.config.WORK_START +
        self.simulation_time
    ) % self.config.MINUTES_PER_DAY

    return total

  def is_working_hours(self):

    minute = self.current_minute_of_day()

    return (
        self.config.WORK_START
        <= minute
        < self.config.WORK_END
    )

  def minutes_until_next_work_start(self):

    minute = self.current_minute_of_day()

    if minute < self.config.WORK_START:
        return self.config.WORK_START - minute

    if minute >= self.config.WORK_END:
        return (
            self.config.MINUTES_PER_DAY
            - minute
            + self.config.WORK_START
        )

    return 0

  def next_work_start_time(self):
    return self.simulation_time + self.minutes_until_next_work_start()
  
  @staticmethod
  def format_sim_time(simulation_time: int) -> str:

    config = Config()

    day = (
        config.WORK_START + simulation_time
    ) // config.MINUTES_PER_DAY + 1

    minutes_since_day_start = (
        simulation_time % config.MINUTES_PER_DAY
    )

    total_minutes = (
        config.WORK_START + minutes_since_day_start
    )

    total_minutes %= config.MINUTES_PER_DAY

    hours = total_minutes // 60
    minutes = total_minutes % 60

    return f"Day {day}  {hours:02d}:{minutes:02d}"
