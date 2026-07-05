class Renderer {

    render(event) {

        let html = "";

        html += `<h3>Time ${event.Time}</h3>`;
        html += `<p>Day ${event.Day}</p>`;
        html += `<p>${event.Event}</p>`;

        html += "<hr>";

        html += "<h2>Truck Heads</h2>";

        for(const key in event){

            if(key.startsWith("Truck ")){

                html += `<p>${key}: ${event[key]}</p>`;

            }

        }

        html += "<hr>";

        html += "<h2>Tanks</h2>";

        for(const key in event){

            if(key.startsWith("Tank ")){

                html += `<p>${key}: ${event[key]}</p>`;

            }

        }

        document.getElementById("currentEvent").innerHTML = html;

    }

}