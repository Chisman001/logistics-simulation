async function loadSimulation(){

    const response = await fetch('/static/simulation_events.csv');

    const text = await response.text();

    return parseCSV(text);
}

function parseCSV(text){

    const lines = text.trim().split("\n");

    const headers = lines[0].split(",");

    const events = [];

    for(let i=1;i<lines.length;i++){

        const values = lines[i].split(",");

        const row = {};

        headers.forEach((header,index)=>{

            row[header]=values[index];

        });

        events.push(row);

    }

    return events;

}