from flask import Flask, render_template, request, jsonify

from config import Config
from engine.simulation import Simulator
import shutil
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/simulate", methods=["POST"])
def simulate():

    data = request.get_json()

    config = Config()

    config.NUM_TRUCK_HEADS = data["trucks"]
    config.NUM_TANKS = data["tanks"]
    config.SIMULATION_DAYS = data["days"]

    simulator = Simulator(config)

    simulator.run()
    shutil.copy(
        "simulation_events.csv",
        "static/simulation_events.csv"
        )

    return jsonify({
        "success": True
    })


if __name__ == "__main__":
    app.run(debug=True)