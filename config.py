# config.py

# MAVLink
MAVLINK_PORT = "/dev/serial0"
BAUDRATE = 921600

# Drone identity (change to 2,3 for other drones later)
DRONE_ID = 3

# Takeoff altitude (meters)
TAKEOFF_ALT = 3.0

# Formation update rate (seconds)
FORMATION_DT = 0.5

# Flask laptop IP (receiver of telemetry)
FLASK_IP = "192.168.137.1"
FLASK_TELEMETRY_PORT = 7000

# UDP command port (this drone listens here)
CMD_PORT = 6000

# -------- ROTATION CONFIG --------
ROTATION_PERIOD = 80.0   # seconds for one full 360° rotation