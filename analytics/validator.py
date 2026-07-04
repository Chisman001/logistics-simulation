from dataclasses import dataclass, field

from engine.clock import SimulationClock


@dataclass
class ValidationResult:
  passed: bool = True
  checks: list = field(default_factory=list)
  total_gap_minutes: int = 0
  gap_periods: list = field(default_factory=list)
  overlap_violations: list = field(default_factory=list)
  truck_hour_violations: list = field(default_factory=list)
  arrival_violations: list = field(default_factory=list)


def compute_coverage_gaps(intervals, sim_duration, tank_duration):
  if sim_duration <= 0:
    return 0, []

  if not intervals:
    return sim_duration, [(0, sim_duration)]

  covered = []
  for interval in intervals:
    start = interval["start"]
    end = interval["end"] if interval["end"] is not None else start + tank_duration
    covered.append((start, end))

  covered.sort()
  merged = [covered[0]]
  for start, end in covered[1:]:
    if start <= merged[-1][1]:
      merged[-1] = (merged[-1][0], max(merged[-1][1], end))
    else:
      merged.append((start, end))

  gap_total = 0
  gap_periods = []
  cursor = covered[0][0]  
  for start, end in merged:
    if start > cursor:
      gap_periods.append((cursor, start))
      gap_total += start - cursor
    cursor = max(cursor, end)

  if cursor < sim_duration:
    gap_periods.append((cursor, sim_duration))
    gap_total += sim_duration - cursor

  return gap_total, gap_periods


def find_overlap_violations(intervals, safety_window, tank_duration):
  violations = []
  sorted_intervals = sorted(intervals, key=lambda item: item["start"])

  for i, first in enumerate(sorted_intervals):
    first_end = first["end"] if first["end"] is not None else first["start"] + tank_duration
    for second in sorted_intervals[i + 1:]:
      second_end = (
          second["end"] if second["end"] is not None
          else second["start"] + tank_duration
      )
      if second["start"] >= first_end:
        break

      overlap_start = max(first["start"], second["start"])
      overlap_end = min(first_end, second_end)
      overlap = overlap_end - overlap_start
      if overlap > safety_window:
        violations.append({
            "tank_a": first["tank_id"],
            "tank_b": second["tank_id"],
            "overlap": overlap,
            "start": overlap_start,
        })

  return violations


class SimulationValidator:
  def __init__(self, statistics, config):
    self.statistics = statistics
    self.config = config
    self.result = ValidationResult()

  def validate(self):
    self.result = ValidationResult()
    self._check_starts_vs_empties()
    self._check_supply_vs_expected()
    self._check_coverage_gaps()
    self._check_reported_vs_actual_downtime()
    self._check_overlap_violations()
    self._check_truck_work_hours()
    self._check_supply_before_arrival()
    return self.result

  def _add_check(self, name, passed, detail):
    self.result.checks.append({"name": name, "passed": passed, "detail": detail})
    if not passed:
      self.result.passed = False

  def _check_starts_vs_empties(self):
    starts = self.statistics.supply_operations
    empties = self.statistics.completed_deliveries
    max_allowed = self.config.NUM_TANKS

    diff = abs(starts - empties)

    passed = diff <= max_allowed
    self._add_check(
        "Starts vs empties",
        passed,
        f"supply_operations={starts}, completed_deliveries={empties} (diff={diff})",
    )

  def _check_supply_vs_expected(self):
    sim_duration = self.statistics.simulation_duration
    handover_interval = self.config.TANK_DURATION - self.config.SAFETY_WINDOW
    expected = (sim_duration / self.config.TANK_DURATION) if handover_interval else 0
    actual = self.statistics.supply_operations
    ratio = actual / expected if expected else 0
    passed = ratio >= 0.9
    self._add_check(
        "Supply vs expected throughput",
        passed,
        f"actual={actual}, expected~={expected:.1f}, ratio={ratio:.2f}",
    )

  def _check_coverage_gaps(self):
    gap_total, gap_periods = compute_coverage_gaps(
        self.statistics.supply_intervals,
        self.statistics.simulation_duration,
        self.config.TANK_DURATION,
    )
    self.result.total_gap_minutes = gap_total
    self.result.gap_periods = gap_periods
    self._add_check(
        "Consumer coverage",
        gap_total == 0,
        f"actual coverage gaps={gap_total} min across {len(gap_periods)} period(s)",
    )

  def _check_reported_vs_actual_downtime(self):
    reported = self.statistics.total_consumer_downtime
    actual = self.result.total_gap_minutes
    difference = abs(reported - actual)
    passed = difference <= self.config.SAFETY_WINDOW
    self._add_check(
        "Reported vs actual downtime",
        passed,
        f"reported={reported} min, validator gaps={actual} min",
    )

  def _check_overlap_violations(self):
    violations = find_overlap_violations(
        self.statistics.supply_intervals,
        self.config.SAFETY_WINDOW,
        self.config.TANK_DURATION,
    )
    self.result.overlap_violations = violations
    self._add_check(
        "Overlap within safety window",
        len(violations) == 0,
        f"{len(violations)} overlap violation(s) > {self.config.SAFETY_WINDOW} min",
    )

  def _check_truck_work_hours(self):
    violations = []
    for movement in self.statistics.truck_movements:
      minute_of_day = (movement["sim_time"] + self.config.WORK_START) % self.config.MINUTES_PER_DAY
      if not (self.config.WORK_START <= minute_of_day < self.config.WORK_END):
        violations.append(movement)

    self.result.truck_hour_violations = violations
    self._add_check(
        "Truck movements within work hours",
        len(violations) == 0,
        f"{len(violations)} movement(s) outside 06:00-18:00",
    )

  def _check_supply_before_arrival(self):
    violations = []
    for interval in self.statistics.supply_intervals:
      arrived_at = interval.get("arrived_at")
      if arrived_at is None:
        continue
      if interval["start"] < arrived_at:
        violations.append(interval)

    self.result.arrival_violations = violations
    self._add_check(
        "Supply starts after arrival",
        len(violations) == 0,
        f"{len(violations)} supply start(s) before tank arrival",
    )

  def print_report(self):
    print()
    print("=" * 40)
    print("Validation")
    print("=" * 40)
    print(f"Overall: {'PASS' if self.result.passed else 'FAIL'}")
    print()

    for check in self.result.checks:
      status = "PASS" if check["passed"] else "FAIL"
      print(f"  [{status}] {check['name']}: {check['detail']}")

    if self.result.gap_periods:
      print()
      print("  Coverage gap periods:")
      for start, end in self.result.gap_periods[:10]:
        print(
            f"    {SimulationClock.format_sim_time(start)}"
            f" - {SimulationClock.format_sim_time(end)}"
            f" ({end - start} min)"
        )
      if len(self.result.gap_periods) > 10:
        print(f"    ... and {len(self.result.gap_periods) - 10} more")

  def print_supply_timeline(self):
    print()
    print("=" * 40)
    print("Supply Timeline")
    print("=" * 40)

    events = []
    for interval in self.statistics.supply_intervals:
      events.append((
          interval["start"],
          f"Tank {interval['tank_id']} started supplying",
      ))
      if interval["end"] is not None:
        events.append((
            interval["end"],
            f"Tank {interval['tank_id']} empty",
        ))

    for time, message in sorted(events):
      print(f"  {SimulationClock.format_sim_time(time)}  {message}")

    print()
    print(f"  Total supply starts: {self.statistics.supply_operations}")
