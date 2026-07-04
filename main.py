# main.py

import time, threading
import collections, collections.abc
if not hasattr(collections, "MutableMapping"):
    collections.MutableMapping = collections.abc.MutableMapping

from config import *
from mavlink_iface import connect_vehicle, arm_and_takeoff, goto_position, rtl
from formation import get_target
from telemetry import telemetry_loop
from swarm_comm import start_cmd_listener
from safety import can_fly


# ---------------- CONNECT ----------------
vehicle = connect_vehicle(MAVLINK_PORT, BAUDRATE)

# Flight phases:
# IDLE -> TAKEOFF -> HOVER -> FORMATION
flight_phase = "IDLE"
current_formation = None

t0 = time.time()

# Control tuning
ALT_HOLD_TOL = 0.4     # meters (altitude deadband)
CMD_RATE = 2.0         # seconds (slow = smooth)
HOVER_TIME = 3.0       # seconds to stabilize after takeoff


# ---------------- COMMAND HANDLER ----------------
def handle_cmd(cmd):
    global flight_phase, current_formation, t0

    print("[CMD]", cmd)

    if cmd in ["triangle", "line", "steps"]:
        current_formation = cmd

        if flight_phase == "IDLE":
            if not can_fly(vehicle):
                print("[SAFETY] Vehicle not ready")
                return

            print("[FLIGHT] TAKEOFF phase")
            flight_phase = "TAKEOFF"

            arm_and_takeoff(vehicle, TAKEOFF_ALT)

            print("[FLIGHT] HOVER stabilization")
            flight_phase = "HOVER"
            time.sleep(HOVER_TIME)

            print("[FLIGHT] FORMATION mode")
            t0 = time.time()  # reset formation timer
            flight_phase = "FORMATION"

    elif cmd == "rtl":
        print("[FLIGHT] RTL")
        rtl(vehicle)
        flight_phase = "IDLE"
        current_formation = None


# ---------------- TELEMETRY ----------------
threading.Thread(
    target=telemetry_loop,
    args=(vehicle, DRONE_ID, FLASK_IP, FLASK_TELEMETRY_PORT),
    daemon=True
).start()


# ---------------- COMMAND LISTENER ----------------
threading.Thread(
    target=start_cmd_listener,
    args=(CMD_PORT, handle_cmd),
    daemon=True
).start()


print("[SWARM READY]")


# ---------------- MAIN FLIGHT LOOP ----------------
while True:
    if flight_phase == "FORMATION" and current_formation:
        t = time.time() - t0

        lat, lon, target_alt = get_target(
            vehicle,
            current_formation,
            TAKEOFF_ALT,
            t,
            DRONE_ID
        )

        current_alt = vehicle.location.global_relative_frame.alt

        # ---- ALTITUDE DEADZONE ----
        if abs(current_alt - target_alt) > ALT_HOLD_TOL:
            goto_position(vehicle, lat, lon, target_alt)
        else:
            # Hold altitude, adjust lateral only
            goto_position(vehicle, lat, lon, current_alt)

    time.sleep(CMD_RATE)
