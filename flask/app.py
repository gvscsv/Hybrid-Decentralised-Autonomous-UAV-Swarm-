from flask import Flask, render_template, jsonify
import socket, threading, json

app = Flask(__name__)
drones = {}

# ---------------- UDP TELEMETRY RECEIVER ----------------
def rx():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", 7000))
    print("[FLASK] Listening for telemetry on UDP 7000")

    while True:
        data, _ = s.recvfrom(2048)
        msg = json.loads(data.decode())
        drones[msg["id"]] = msg

threading.Thread(target=rx, daemon=True).start()

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("map.html")

@app.route("/data")
def data():
    # Build neighbors dynamically (visualization only)
    ids = list(drones.keys())
    out = {}

    for i in ids:
        out[i] = drones[i].copy()
        out[i]["neighbors"] = [j for j in ids if j != i]

    return jsonify(out)

@app.route("/cmd/<c>")
def cmd(c):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ---- CHANGE THESE TO YOUR DRONE IPs ----
    DRONES = [
        "192.168.137.213",
        "192.168.137.227",
        "192.168.137.38"
    ]

    for ip in DRONES:
        s.sendto(json.dumps({"cmd": c}).encode(), (ip, 6000))

    print(f"[FLASK] Sent command '{c}' to {DRONES}")
    return "OK"

# ---------------- RUN SERVER ----------------
app.run(host="0.0.0.0", port=5000, debug=False)
