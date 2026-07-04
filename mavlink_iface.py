# mavlink_iface.py

import time
import collections, collections.abc
if not hasattr(collections, "MutableMapping"):
    collections.MutableMapping = collections.abc.MutableMapping

from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil


def connect_vehicle(port, baud):
    print("[MAV] Connecting...")
    return connect(port, baud=baud, wait_ready=True)


def arm_and_takeoff(vehicle, target_alt):
    print("[MAV] Switching to GUIDED")
    vehicle.mode = VehicleMode("GUIDED")
    while vehicle.mode.name != "GUIDED":
        time.sleep(0.2)

    print("[MAV] Arming")
    vehicle.armed = True
    while not vehicle.armed:
        time.sleep(0.2)

    print("[MAV] Sending TAKEOFF command")

    msg = vehicle.message_factory.command_long_encode(
        0, 0,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0,
        0, 0, 0, 0,
        0, 0,
        target_alt
    )
    vehicle.send_mavlink(msg)
    vehicle.flush()

    # --- WAIT FOR FULL TAKEOFF ---
    while True:
        alt = vehicle.location.global_relative_frame.alt
        print("[TAKEOFF ALT]", round(alt, 2))

        if alt >= target_alt * 0.95:
            print("[MAV] Target altitude reached")
            break

        time.sleep(0.3)

    # --- HOVER STABILIZATION ---
    print("[MAV] Stabilizing hover...")
    time.sleep(3)

def goto_position(vehicle, lat, lon, alt):
    target = LocationGlobalRelative(lat, lon, alt)
    vehicle.simple_goto(target)


def rtl(vehicle):
    print("[MAV] RTL")
    vehicle.mode = VehicleMode("RTL")
