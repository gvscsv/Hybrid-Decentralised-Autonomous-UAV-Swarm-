# formation.py

import math
from config import ROTATION_PERIOD

# Approx conversion: 1 meter ≈ 1e-5 degrees (valid for small distances)
METER_TO_DEG = 1e-5


# ---------- BASE FORMATION SHAPES (METERS) ----------
# Centered equilateral triangle (side ≈ 2 m)
BASE_TRIANGLE = {
    1: (-1.0, -0.6),
    2: ( 1.0, -0.6),
    3: ( 0.0,  1.2),
}

# Straight horizontal line
BASE_LINE = {
    1: (-0.5, 0.0),
    2: ( 0.0, 0.0),
    3: ( 0.5, 0.0),
}


def rotate(x, y, theta):
    """Rotate point (x, y) by angle theta (radians)"""
    xr = x * math.cos(theta) - y * math.sin(theta)
    yr = x * math.sin(theta) + y * math.cos(theta)
    return xr, yr


def get_target(vehicle, formation, base_alt, t, drone_id):
    loc = vehicle.location.global_relative_frame

    # ---------- ROTATION ANGLE ----------
    omega = 2 * math.pi / ROTATION_PERIOD   # rad/sec
    theta = omega * t

    # ---------- FORMATION OFFSET ----------
    if formation == "triangle":
        x, y = BASE_TRIANGLE.get(drone_id, (0.0, 0.0))
        x, y = rotate(x, y, theta)

    elif formation == "line":
        x, y = BASE_LINE.get(drone_id, (0.0, 0.0))

    else:
        x, y = (0.0, 0.0)

    # ---------- GPS CONVERSION ----------
    lat = loc.lat + x * METER_TO_DEG
    lon = loc.lon + y * METER_TO_DEG

    # ---------- ALTITUDE (NATURAL OSCILLATION) ----------
    if formation == "steps":
        # Smooth vertical oscillation (5-second period)
        period = 5.0          # seconds
        amplitude = 2.0       # meters (safe & smooth)

        alt = base_alt + amplitude * math.sin(
            2 * math.pi * t / period
        )
    else:
        alt = base_alt

    return lat, lon, alt
