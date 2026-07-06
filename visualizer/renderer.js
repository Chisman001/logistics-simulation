class Renderer {

    render(state) {
        console.log(state);
        console.log(state.trucks);
        const trucks = state.trucks;
        const tanks = state.tanks;

        const pointA = document.getElementById("pointA");
        const road = document.getElementById("road");
        const pointC = document.getElementById("pointC");

        pointA.innerHTML = "";
        road.innerHTML = "";
        pointC.innerHTML = "";

        this.renderTrucks(trucks, pointA, road, pointC);

        this.renderTanks(tanks, pointA, road, pointC);

        document.getElementById("currentEvent").innerHTML =
        `
        <strong>Time:</strong> ${state.time}<br>
        <strong>Day:</strong> ${state.day}<br>
        <strong>Event:</strong> ${state.event}
        `;
    }

    renderTrucks(trucks, pointA, road, pointC) {

        for(const truck of trucks){
            console.log(truck);
            const div = document.createElement("div");

            div.className = "vehicle";

            div.innerHTML =
                `🚛 Truck ${truck.id}<br>${truck.state}`;

            switch(truck.location){

                case "POINT_A":
                    pointA.appendChild(div);
                    break;

                case "POINT_C":
                    pointC.appendChild(div);
                    break;

                default:
                    road.appendChild(div);
            }

        }

    }

    renderTanks(tanks, pointA, road, pointC){

        for(const tank of tanks){

            const div = document.createElement("div");

            div.className = "vehicle";

            div.innerHTML =
                `🛢 Tank ${tank.id}<br>${tank.state}`;

            switch(tank.location){

                case "POINT_A":
                    pointA.appendChild(div);
                    break;

                case "POINT_C":
                    pointC.appendChild(div);
                    break;

                default:
                    road.appendChild(div);
            }

        }

    }

}