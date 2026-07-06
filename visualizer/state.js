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

    for (const key in event) {

        if (key.startsWith("Truck ")) {

            const parts = event[key].split("|");

            this.trucks.push({
                id: parseInt(key.replace("Truck ", "")),
                state: parts[0].trim(),
                location: parts[1].trim(),
                tank: parts[2].replace("Tank:", "").trim()
            });

        }

        if (key.startsWith("Tank ")) {

            const parts = event[key].split("|");

            this.tanks.push({
                id: parseInt(key.replace("Tank ", "")),
                state: parts[0].trim(),
                location: parts[1].trim(),
                truck: parts[2].replace("Truck:", "").trim()
            });

        }

    }
        console.log(this.trucks);
        console.log(this.tanks);
    }
}