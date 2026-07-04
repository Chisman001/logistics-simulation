import unittest

from engine.event import Event
from engine.simulation import Simulator
from models.enums import EventType, Location, TankState, TruckState


class SupplyFlowTests(unittest.TestCase):
    def make_simulator(self):
        simulator = Simulator()
        simulator.create_tanks()
        simulator.create_truck_heads()
        return simulator

    def test_truck_arrival_places_tank_in_waiting_state(self):
        simulator = self.make_simulator()
        tank = simulator.tanks[1]
        truck = simulator.truck_heads[1]

        truck.state = TruckState.IDLE_AT_A
        truck.location = Location.POINT_A
        tank.state = TankState.READY_AT_A
        tank.location = Location.POINT_A

        previous_tank = simulator.tanks[2]
        previous_tank.state = TankState.SUPPLYING
        previous_tank.supply_started_at = 50
        simulator.active_supply_tank = previous_tank

        event = Event(
            simulation_time=100,
            event_type=EventType.TRUCK_ARRIVED,
            truck_head_id=truck.id,
            tank_id=tank.id,
        )

        simulator.clock.simulation_time = 100
        simulator.handle_truck_arrived(event)

        self.assertEqual(tank.state, TankState.WAITING_AT_C)
        self.assertEqual(tank.location, Location.POINT_C)
        self.assertEqual(simulator.statistics.supply_operations, 0)
        self.assertIs(simulator.pending_supply_tank, tank)

    def test_supply_started_event_marks_tank_as_supplying(self):
        simulator = self.make_simulator()
        tank = simulator.tanks[1]
        tank.state = TankState.WAITING_AT_C
        tank.location = Location.POINT_C

        event = Event(
            simulation_time=120,
            event_type=EventType.SUPPLY_STARTED,
            tank_id=tank.id,
        )

        simulator.handle_supply_started(event)

        self.assertEqual(tank.state, TankState.SUPPLYING)
        self.assertEqual(simulator.statistics.supply_operations, 1)

    def test_first_tank_at_c_starts_immediately(self):
        simulator = self.make_simulator()
        tank = simulator.tanks[1]
        tank.state = TankState.WAITING_AT_C
        tank.location = Location.POINT_C
        tank.arrived_at = 200
        simulator.waiting_tanks_at_c.append(tank)
        simulator.clock.simulation_time = 200

        simulator.schedule_supply_start(tank, 200)

        self.assertEqual(tank.state, TankState.SUPPLYING)
        self.assertEqual(tank.supply_started_at, 200)
        self.assertEqual(simulator.statistics.safety_violations, 0)

    def test_early_arrival_waits_for_connection_slot(self):
        simulator = self.make_simulator()
        previous = simulator.tanks[2]
        previous.state = TankState.SUPPLYING
        previous.supply_started_at = 100
        simulator.active_supply_tank = previous

        tank = simulator.tanks[1]
        tank.state = TankState.WAITING_AT_C
        tank.location = Location.POINT_C
        tank.arrived_at = 150
        simulator.waiting_tanks_at_c.append(tank)
        simulator.clock.simulation_time = 150

        simulator.schedule_supply_start(tank, 150)

        required_connection = 100 + simulator.config.TANK_DURATION - simulator.config.SAFETY_WINDOW
        self.assertEqual(tank.state, TankState.WAITING_AT_C)
        self.assertIs(simulator.pending_supply_tank, tank)
        self.assertEqual(simulator.statistics.safety_violations, 0)
        self.assertEqual(required_connection, 520)

    def test_late_arrival_records_safety_violation(self):
        simulator = self.make_simulator()
        previous = simulator.tanks[2]
        previous.state = TankState.SUPPLYING
        previous.supply_started_at = 100
        simulator.active_supply_tank = previous

        tank = simulator.tanks[1]
        tank.state = TankState.WAITING_AT_C
        tank.location = Location.POINT_C
        tank.arrived_at = 650
        simulator.waiting_tanks_at_c.append(tank)
        simulator.clock.simulation_time = 650

        simulator.schedule_supply_start(tank, 650)

        self.assertEqual(tank.state, TankState.SUPPLYING)
        self.assertEqual(simulator.statistics.safety_violations, 1)
        self.assertGreater(simulator.statistics.safety_delays[0], 0)

    def test_arrival_after_previous_empty_records_downtime(self):
        simulator = self.make_simulator()
        previous = simulator.tanks[2]
        previous.state = TankState.SUPPLYING
        previous.supply_started_at = 100
        simulator.active_supply_tank = previous

        tank = simulator.tanks[1]
        tank.state = TankState.WAITING_AT_C
        tank.location = Location.POINT_C
        tank.arrived_at = 700
        simulator.waiting_tanks_at_c.append(tank)
        simulator.clock.simulation_time = 700

        simulator.schedule_supply_start(tank, 700)

        expected_empty = 100 + simulator.config.TANK_DURATION
        self.assertEqual(
            simulator.statistics.total_consumer_downtime,
            700 - expected_empty,
        )

    def test_empty_clears_active_and_promotes_waiting_tank(self):
        simulator = self.make_simulator()
        active = simulator.tanks[1]
        active.state = TankState.SUPPLYING
        active.supply_started_at = 100
        active.departed_at = 0
        simulator.active_supply_tank = active

        waiting = simulator.tanks[2]
        waiting.state = TankState.WAITING_AT_C
        waiting.location = Location.POINT_C
        waiting.arrived_at = 500
        simulator.waiting_tanks_at_c.append(waiting)

        event = Event(
            simulation_time=580,
            event_type=EventType.TANK_EMPTY,
            tank_id=active.id,
        )
        simulator.clock.simulation_time = 580
        simulator.handle_tank_empty(event)

        self.assertIs(simulator.active_supply_tank, waiting)
        self.assertEqual(waiting.state, TankState.SUPPLYING)

    def test_overlap_period_keeps_successor_as_active(self):
        simulator = self.make_simulator()
        predecessor = simulator.tanks[1]
        predecessor.state = TankState.SUPPLYING
        predecessor.supply_started_at = 100
        predecessor.departed_at = 0

        successor = simulator.tanks[2]
        successor.state = TankState.SUPPLYING
        successor.supply_started_at = 520
        simulator.active_supply_tank = successor

        event = Event(
            simulation_time=580,
            event_type=EventType.TANK_EMPTY,
            tank_id=predecessor.id,
        )
        simulator.clock.simulation_time = 580
        simulator.handle_tank_empty(event)

        self.assertIs(simulator.active_supply_tank, successor)

    def test_has_successor_at_c_when_tank_in_transit(self):
        simulator = self.make_simulator()
        tank = simulator.tanks[1]
        tank.state = TankState.IN_TRANSIT_TO_C

        self.assertTrue(simulator.has_successor_at_c())

    def test_chain_break_records_downtime_when_supply_resumes(self):
        simulator = self.make_simulator()
        active = simulator.tanks[1]
        active.state = TankState.SUPPLYING
        active.supply_started_at = 100
        active.departed_at = 0
        simulator.active_supply_tank = active

        empty_event = Event(
            simulation_time=580,
            event_type=EventType.TANK_EMPTY,
            tank_id=active.id,
        )
        simulator.clock.simulation_time = 580
        simulator.handle_tank_empty(empty_event)

        self.assertIsNotNone(simulator.supply_gap_started_at)
        self.assertEqual(simulator.statistics.total_consumer_downtime, 0)

        replacement = simulator.tanks[2]
        replacement.state = TankState.WAITING_AT_C
        replacement.location = Location.POINT_C
        replacement.arrived_at = 700
        simulator.waiting_tanks_at_c.append(replacement)
        simulator.clock.simulation_time = 700

        simulator.schedule_supply_start(replacement, 700)

        self.assertEqual(simulator.statistics.total_consumer_downtime, 120)
        self.assertIsNone(simulator.supply_gap_started_at)

    def test_ready_tank_is_prepositioned_for_upcoming_handover(self):
        simulator = self.make_simulator()
        active = simulator.tanks[1]
        active.state = TankState.SUPPLYING
        active.supply_started_at = 100
        simulator.active_supply_tank = active

        ready = simulator.tanks[2]
        ready.state = TankState.READY_AT_A
        ready.location = Location.POINT_A
        simulator.clock.simulation_time = 150

        simulator.preposition_ready_tanks_for_next_handover()

        self.assertEqual(ready.state, TankState.WAITING_AT_C)
        self.assertEqual(ready.location, Location.POINT_C)
        self.assertIn(ready, simulator.waiting_tanks_at_c)


if __name__ == "__main__":
    unittest.main()
