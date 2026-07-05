class Player {

    constructor() {
        this.currentFrame = 0;
        this.events = [];
        this.playing = false;
        this.timer = null;
    }

    loadEvents(data) {
        this.events = data;
        this.currentFrame = 0;
    }

    currentEvent() {
        return this.events[this.currentFrame];
    }

    nextFrame() {

        if (this.currentFrame >= this.events.length - 1) {
            this.stop();
            return;
        }

        this.currentFrame++;

        render(this.currentEvent());
    }

    previousFrame() {

        if (this.currentFrame <= 0)
            return;

        this.currentFrame--;

        render(this.currentEvent());
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

const player = new Player();