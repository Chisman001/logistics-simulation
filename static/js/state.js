class WorldState {

    constructor() {

        this.time = 0;
        this.day = 1;
        this.event = "";
        this.trucks = {};
        this.tanks ={};

    }

    load(event) {

    this.time = Number(event.Time);
    this.day = Number(event.Day);
    this.event = event.Event;

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

          const id = parseInt(key.replace("Truck ", ""));

            if (!this.trucks[id]) {

                this.trucks[id] = {

                    id: id,

                    x: position.x,
                    y: position.y,

                    targetX: position.x,
                    targetY: position.y

                };

            }

            const truck = this.trucks[id];

            truck.state = parts[0].trim();
            truck.location = location;
            truck.tank = parts[2].replace("Tank:", "").trim();

            truck.targetX = position.x;
            truck.targetY = position.y;

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

            const id = parseInt(key.replace("Tank ", ""));

            if (!this.tanks[id]) {

                this.tanks[id] = {

                    id: id,

                    x: position.x,
                    y: position.y,

                    targetX: position.x,
                    targetY: position.y

                };

            }

            const tank = this.tanks[id];

            tank.state = parts[0].trim();
            tank.location = location;
            tank.truck = parts[2].replace("Truck:", "").trim();

            tank.targetX = position.x;
            tank.targetY = position.y;

        }

    }
        console.log(this.trucks);
        console.log(this.tanks);
    }
}