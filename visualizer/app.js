async function main() {

    const events = await loadSimulation();

    const renderer = new Renderer();

    const player = new Player(renderer);

    player.loadEvents(events);

    document.getElementById("summary").innerHTML = `
        <strong>Total Events:</strong> ${events.length}<br>
        <strong>Simulation Days:</strong> ${events[events.length - 1].Day}
    `;

}
main()