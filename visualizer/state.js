class WorldState {

    constructor() {

        this.time = 0;
        this.day = 1;
        this.event = "";

        this.trucks = [];
        this.tanks = [];

    }

    load(event) {

    this.time = Number(event.Time);
    this.day = Number(event.Day);
    this.event = event.Event;

    this.trucks = [];
    this.tanks = [];

    const truckCounts = {
        POINT_A: 0,
        POINT_C: 0,
        IN_TRANSIT_TO_A: 0,
        IN_TRANSIT_TO_C: 0
    };

    const tankCounts = {
        POINT_A: 0,
        POINT_C: 0,
        IN_TRANSIT_TO_A: 0,
        IN_TRANSIT_TO_C: 0
    };

    for (const key in event) {

        if (key.startsWith("Truck ")) {

            const parts = event[key].split("|");

            const location = parts[1].trim();
            if (!(location in truckCounts)) {
                truckCounts[location] = 0;
            }
          const position = Layout.truckPosition(
              location,
              truckCounts[location]++
          );

          this.trucks.push({

              id: parseInt(key.replace("Truck ", "")),

              state: parts[0].trim(),

              location: location,

              tank: parts[2].replace("Tank:", "").trim(),

              x: position.x,
              y: position.y,

              targetX: position.x,
              targetY: position.y

          });

        }

        if (key.startsWith("Tank ")) {

            const parts = event[key].split("|");

            const location = parts[1].trim();
            if (!(location in tankCounts)) {
                tankCounts[location] = 0;
            }
            const position = Layout.tankPosition(
                location,
                tankCounts[location]++
            );

            this.tanks.push({

                id: parseInt(key.replace("Tank ", "")),

                state: parts[0].trim(),

                location: location,

                truck: parts[2].replace("Truck:", "").trim(),
                x: position.x,
                y: position.y,

                targetX: position.x,
                targetY: position.y

            });

        }

    }
        console.log(this.trucks);
        console.log(this.tanks);
    }
}