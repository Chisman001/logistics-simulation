from optimization.search import Search


def main():

    search = Search()

    best, results = search.search()

    print()
    print("=" * 40)
    print("Optimization Result")
    print("=" * 40)

    print(f"Scenarios Tested: {len(results)}")
    print(f"Best Score: {best.score}")
    scenario = best.scenario

    print()
    print("Best Configuration")
    print("-------------------")
    print(f"Tanks: {scenario.num_tanks}")
    print(f"Truck Heads: {scenario.num_truck_heads}")
    print(f"Tank Capacity: {scenario.tank_capacity}")
    print(f"Travel Time: {scenario.travel_time}")
    print(f"Fill Time: {scenario.fill_time}")
    print(f"Safety Window: {scenario.safety_window}")
    summary = best.metrics.simulation_summary()

    print(f"Deliveries: {summary['Completed Deliveries']}")
    print(f"Dispatches: {summary['Dispatches']}")
    print(f"Returns: {summary['Returns']}")
    
    tank = best.metrics.tank_performance()

    print(f"Average Tank Wait: {tank['Average Tank Wait']:.2f}")
    print(f"Average Cycle Time: {tank['Average Cycle Time']:.2f}")

if __name__ == "__main__":
    main()