class Renderer {

    render(state) {
        console.log(state);
        console.log(state.trucks);
        const trucks = state.trucks;
        const tanks = state.tanks;

        const pointATrucks = document.getElementById("pointATrucks");
        const pointATanks = document.getElementById("pointATanks");

        const roadTrucks = document.getElementById("roadTrucks");
        const roadTanks = document.getElementById("roadTanks");

        const pointCTrucks = document.getElementById("pointCTrucks");
        const pointCTanks = document.getElementById("pointCTanks");

        pointATrucks.innerHTML = "";
        pointATanks.innerHTML = "";

        roadTrucks.innerHTML = "";
        roadTanks.innerHTML = "";

        pointCTrucks.innerHTML = "";
        pointCTanks.innerHTML = "";

        this.renderTrucks(
          trucks,
          pointATrucks,
          roadTrucks,
          pointCTrucks
        );

        this.renderTanks(
          tanks,
          pointATanks,
          roadTanks,
          pointCTanks
        );

        document.getElementById("currentEvent").innerHTML =
        `
        <strong>Time:</strong> ${state.time}<br>
        <strong>Day:</strong> ${state.day}<br>
        <strong>Event:</strong> ${state.event}
        `;
    }

    renderTrucks(trucks, pointATrucks, roadTrucks, pointCTrucks) {

        for (const truck of Object.values(trucks)) {
            console.log(truck);
            const div = document.createElement("div");
            div.style.background = this.stateColor(truck.state);

            div.className = "truck";

            div.innerHTML = `
            <div class="title">🚛 Truck ${truck.id}</div>

            <div class="status">${this.formatState(truck.state)}</div>

            <div class="small">
            Tank: ${truck.tank}
            </div>
            `;

            switch(truck.location){

                case "POINT_A":
                    pointATrucks.appendChild(div);
                    break;

                case "POINT_C":
                    pointCTrucks.appendChild(div);
                    break;

                default:
                    roadTrucks.appendChild(div);
            }

        }

    }

    renderTanks(tanks, pointATanks, roadTanks, pointCTanks){

        for (const tank of Object.values(tanks)) {

            const div = document.createElement("div");
            div.style.background = this.stateColor(tank.state);

            div.className = "tank";

            div.innerHTML = `
            <div class="title">🛢 Tank ${tank.id}</div>

            <div class="status">${this.formatState(tank.state)}</div>

            <div class="small">
            Truck: ${tank.truck}
            </div>
            `;

            switch(tank.location){

                case "POINT_A":
                    pointATanks.appendChild(div);
                    break;

                case "POINT_C":
                    pointCTanks.appendChild(div);
                    break;

                default:
                    roadTanks.appendChild(div);
            }

        }

    }

    stateColor(state) {

        if (state.includes("IDLE"))
            return "#22c55e";

        if (state.includes("FILL"))
            return "#3b82f6";

        if (state.includes("DRIVING"))
            return "#f59e0b";

        if (state.includes("SUPPLY"))
            return "#ef4444";

        if (state.includes("EMPTY"))
            return "#6b7280";

        if (state.includes("RETURN"))
            return "#8b5cf6";

        if (state.includes("WAIT"))
            return "#06b6d4";

        return "#374151";

    }

    formatState(state) {

        return state
            .replaceAll("_", " ")
            .toLowerCase()
            .replace(/\b\w/g, c => c.toUpperCase());

    }

}