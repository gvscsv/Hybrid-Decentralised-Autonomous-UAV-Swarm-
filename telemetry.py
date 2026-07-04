# telemetry.py

import socket, json, time


def telemetry_loop(vehicle, drone_id, flask_ip, flask_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        loc = vehicle.location.global_relative_frame

        if loc.lat and loc.lon:
            msg = {
                "id": drone_id,
                "lat": loc.lat,
                "lon": loc.lon,
                "alt": loc.alt,
                "mode": vehicle.mode.name
            }

            sock.sendto(
                json.dumps(msg).encode(),
                (flask_ip, flask_port)
            )

        time.sleep(0.5)
