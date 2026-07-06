async function loadReplay() {

    const events = await loadSimulation();

    const renderer = new CanvasRenderer();

    const player = new Player(renderer);

    player.loadEvents(events);

    renderer.animate(player.state, player);

    document.getElementById("play").onclick = () => {

        player.play();

    };

    document.getElementById("pause").onclick = () => {

        player.stop();

    };

    document.getElementById("next").onclick = () => {

        player.nextFrame();

    };

    document.getElementById("previous").onclick = () => {

        player.previousFrame();

    };

    document.getElementById("summary").innerHTML = `

        <strong>Total Events:</strong> ${events.length}<br>

        <strong>Simulation Days:</strong> ${events[events.length - 1].Day}

    `;

}

function getSimulationSettings() {

    return {

        trucks: Number(
            document.getElementById("truckCount").value
        ),

        tanks: Number(
            document.getElementById("tankCount").value
        ),

        days: Number(
            document.getElementById("simulationDays").value
        )

    };

}

document
    .getElementById("runSimulation")
    .onclick = async () => {

        const settings = getSimulationSettings();

        const response = await fetch("/simulate", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(settings)

        });

        const result = await response.json();

        if (!result.success) {

            alert("Simulation failed.");

            return;

        }

        await loadReplay();

    };

  document
    .getElementById("loadReplay")
    .onclick = async () => {

        await loadReplay();

};