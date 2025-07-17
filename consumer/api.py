from flask import Flask, jsonify, render_template
from threading import Thread
from gps_consumer import start_consumer, latest_positions

app = Flask(__name__, template_folder="templates")

@app.route("/live")
def live_positions():
    """Return latest GPS positions of all cars"""
    return jsonify(latest_positions)

@app.route("/")
def map_view():
    """Show live map"""
    return render_template("map.html")

if __name__ == "__main__":
    # Run Kafka consumer in a separate thread
    t = Thread(target=start_consumer, daemon=True)
    t.start()

    # Start Flask API on port 5001
    app.run(host="0.0.0.0", port=5001)
