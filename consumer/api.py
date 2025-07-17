from flask import Flask, jsonify, render_template
from threading import Thread
from gps_consumer import start_consumer, latest_positions  # only current GPS

app = Flask(__name__, template_folder="templates")

@app.route("/live")
def live_positions():
    return jsonify({
        "positions": latest_positions   # ✅ only current GPS, no full route
    })

@app.route("/")
def map_view():
    return render_template("map.html")

if __name__ == "__main__":
    Thread(target=start_consumer, daemon=True).start()
    app.run(host="0.0.0.0", port=5001)
