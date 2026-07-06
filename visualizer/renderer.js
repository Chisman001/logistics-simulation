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

        for(const truck of trucks){
            console.log(truck);
            const div = document.createElement("div");

            div.className = "truck";

            div.innerHTML = `
            🚛
            <div>Truck ${truck.id}</div>
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

        for(const tank of tanks){

            const div = document.createElement("div");

            div.className = "tank";

            div.innerHTML = `
            🛢
            <div>Tank ${tank.id}</div>
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

}