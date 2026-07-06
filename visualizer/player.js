class Player {

    constructor(renderer) {
        this.renderer = renderer;

        this.state = new WorldState();    
        this.currentFrame = 0;
        this.events = [];
        this.playing = false;
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

    update() {

        this.state.load(this.currentEvent());

    }

    nextFrame() {

        if (this.currentFrame >= this.events.length - 1) {
            this.stop();
            return;
        }

        this.currentFrame++;

        this.update();

    }

    previousFrame() {

        if (this.currentFrame <= 0)
            return;

        this.currentFrame--;

        this.update();

    }

    play() {

        if (this.playing)
            return;

        this.playing = true;

        this.timer = setInterval(() => {

            this.nextFrame();

        }, 250);

    }

    stop() {

        this.playing = false;

        clearInterval(this.timer);

    }

}