import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, render_template
from threading import Thread
from gps_consumer import start_consumer, latest_positions
from producer.fetch_route import route_points  # ✅ now works


app = Flask(__name__, template_folder="templates")

@app.route("/live")
def live_positions():
    """Return latest GPS positions + full route"""
    return jsonify({
        "positions": latest_positions,
        "route": route_points  # full route coordinates
    })

@app.route("/")
def map_view():
    return render_template("map.html")

if __name__ == "__main__":
    t = Thread(target=start_consumer, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5001)
