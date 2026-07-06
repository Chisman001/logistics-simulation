class Player {

    constructor(renderer) {
        this.renderer = renderer;

        this.state = new WorldState();    
        this.currentFrame = 0;
        this.events = [];
        this.playing = false;
        this.lastUpdate = 0;
                this.eventInterval = 500; // milliseconds (2 events per second)
        this.timer = null;
    }

    loadEvents(data) {
        this.events = data;
        this.currentFrame = 0;
        this.update();
    }

    currentEvent() {
        return this.events[this.currentFrame];
    }

    loadCurrentEvent() {

        this.state.load(this.currentEvent());

    }

    nextFrame() {

        if (this.currentFrame >= this.events.length - 1) {
            this.stop();
            return;
        }

        this.currentFrame++;

        this.loadCurrentEvent();

          }

    previousFrame() {

        if (this.currentFrame <= 0)
            return;

        this.currentFrame--;

        this.loadCurrentEvent();

    }

    play() {

        this.playing = true;

    }

    stop() {

        this.playing = false;

    }

    update(currentTime) {

        if (!this.playing)
            return;

        if (this.currentFrame >= this.events.length - 1) {

            this.stop();
            return;

        }

        if (currentTime - this.lastUpdate >= this.eventInterval) {

            this.lastUpdate = currentTime;

            this.nextFrame();

        }

    }

    finishedMoving() {

        const tolerance = 2;

        for (const truck of Object.values(this.state.trucks)) {

            if (
                Math.abs(truck.x - truck.targetX) > tolerance ||
                Math.abs(truck.y - truck.targetY) > tolerance
            ) {

                return false;

            }

        }

        for (const tank of Object.values(this.state.tanks)) {

            if (
                Math.abs(tank.x - tank.targetX) > tolerance ||
                Math.abs(tank.y - tank.targetY) > tolerance
            ) {

                return false;

            }

        }

        return true;

    }

    hasMovement(nextEvent) {

    for (const truck of Object.values(this.state.trucks)) {

        const key = `Truck ${truck.id}`;

        if (!nextEvent[key])
            continue;

        const location =
            nextEvent[key].split("|")[1].trim();

        if (location !== truck.location)
            return true;

    }

    for (const tank of Object.values(this.state.tanks)) {

        const key = `Tank ${tank.id}`;

        if (!nextEvent[key])
            continue;

        const location =
            nextEvent[key].split("|")[1].trim();

        if (location !== tank.location)
            return true;

    }

    return false;

}

}