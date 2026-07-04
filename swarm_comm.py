# swarm_comm.py

import socket, json


def start_cmd_listener(port, callback):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))

    print("[CMD] Listening on UDP", port)

    while True:
        data, _ = sock.recvfrom(1024)
        msg = json.loads(data.decode())
        callback(msg["cmd"])
