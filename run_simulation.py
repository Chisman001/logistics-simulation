from config import Config
from engine.simulation import Simulator
import argparse


def run_simulation(
    trucks=5,
    tanks=6,
    days=30
):
    config = Config()

    config.NUM_TRUCK_HEADS = trucks
    config.NUM_TANKS = tanks
    config.SIMULATION_DAYS = days

    simulator = Simulator(config)
    simulator.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--trucks", type=int, default=5)
    parser.add_argument("--tanks", type=int, default=6)
    parser.add_argument("--days", type=int, default=30)

    args = parser.parse_args()

    run_simulation(
        trucks=args.trucks,
        tanks=args.tanks,
        days=args.days
    )