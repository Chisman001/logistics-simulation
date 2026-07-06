import json
from engine.simulator import Simulator 

def main():

    with open("config.json", "r") as file:
        settings = json.load(file)

    print("Running simulation with:")
    print(settings)

    simulator = Simulator()
    simulator.run()

if __name__ == "__main__":
    main()