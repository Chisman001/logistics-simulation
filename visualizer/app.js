async function main() {

    const events = await loadSimulation();

    const renderer = new CanvasRenderer();

    const player = new Player(renderer);

    player.loadEvents(events);
    renderer.animate(player.state);

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

main();