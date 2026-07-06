class CanvasRenderer {

    constructor() {

        this.canvas =
            document.getElementById("simulationCanvas");

        this.ctx =
            this.canvas.getContext("2d");

    }

    render(state) {
        this.clear();

        this.drawBackground(state);

        this.drawMap(state);

        this.drawTrucks(state.trucks);

        this.drawTanks(state.tanks);

        this.drawInfo(state);

    }

    clear() {

        this.ctx.clearRect(

            0,
            0,

            this.canvas.width,

            this.canvas.height

        );

    }

    drawMap(state) {

    const ctx = this.ctx;

    const START_HOUR = 6;

    const hour = this.getHour(state);

    ctx.fillStyle =
        (hour >= 6 && hour < 18)
            ? "black"
            : "white";

    ctx.font = "20px Arial";

    ctx.fillText("Point A", 60, 60);

    ctx.fillText("Road", 560, 60);

    ctx.fillText("Point C", 980, 60);

    ctx.strokeStyle = "#555";
    ctx.lineWidth = 6;

    ctx.beginPath();
    ctx.moveTo(170, 250);
    ctx.lineTo(1000, 250);
    ctx.stroke();
}

    getHour(state) {
        const START_HOUR = 6;
        return (START_HOUR + Math.floor(state.time / 60)) % 24;
    }

    update(state) {

        for (const truck of Object.values(state.trucks)) {

            truck.x = Animator.move(
                truck.x,
                truck.targetX
            );

            truck.y = Animator.move(
                truck.y,
                truck.targetY
            );

        }

        for (const tank of Object.values(state.tanks)) {

            tank.x = Animator.move(
                tank.x,
                tank.targetX
            );

            tank.y = Animator.move(
                tank.y,
                tank.targetY
            );

        }

    }

    animate(state, player) {

        const loop = (time) => {

            player.update(time);

            this.update(state);

            this.render(state);

            requestAnimationFrame(loop);

        };

        requestAnimationFrame(loop);

    }

    drawTrucks(trucks) {

        const ctx = this.ctx;

        for (const truck of Object.values(trucks)) {

            ctx.fillStyle = "#2563eb";

            ctx.fillRect(
                truck.x,
                truck.y,
                70,
                40
            );

            ctx.fillStyle = "white";

            ctx.font = "14px Arial";

            ctx.fillText(
                `T${truck.id}`,
                truck.x + 20,
                truck.y + 25
            );

        }

    }

    drawTanks(tanks) {

        const ctx = this.ctx;

        for (const tank of Object.values(tanks)) {

            ctx.fillStyle = "#16a34a";

            ctx.beginPath();

            ctx.arc(
                tank.x,
                tank.y,
                18,
                0,
                Math.PI * 2
            );

            ctx.fill();

            ctx.fillStyle = "white";

            ctx.font = "12px Arial";

            ctx.fillText(
                tank.id,
                tank.x - 4,
                tank.y + 4
            );

        }

    }

    drawInfo(state) {

        const ctx = this.ctx;

        const START_HOUR = 6;

        const hour = this.getHour(state);

        ctx.fillStyle =
            (hour >= 6 && hour < 18)
                ? "black"
                : "white";

        ctx.font = "18px Arial";

        ctx.fillText(
            `Day: ${state.day}`,
            20,
            30
        );

        ctx.fillText(
            `Time: ${state.time}`,
            180,
            30
        );

        ctx.fillText(
            state.event,
            350,
            30
        );

    }

    drawBackground(state) {

    const ctx = this.ctx;

    // Convert simulation minutes into an hour (0-23)
    const START_HOUR = 6;

    const hour = this.getHour(state);
    if (hour >= 6 && hour < 18) {

        // Day
        ctx.fillStyle = "#f5f5f5";

    } else {

        // Night
        ctx.fillStyle = "#1b1b2f";

    }

    ctx.fillRect(
        0,
        0,
        this.canvas.width,
        this.canvas.height
    );

}

}