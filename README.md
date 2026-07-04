# Hybrid-Decentralised Autonomous UAV Swarm

A decentralized autonomous drone swarm built using **Raspberry Pi 3B companion computers** and **Pixhawk (ArduPilot)** flight controllers.

Each drone operates independently while communicating through a distributed network, enabling autonomous swarm coordination without relying on a centralized controller.

---

## Features

- Decentralized swarm architecture
- Raspberry Pi companion computer integration
- Pixhawk (ArduPilot) flight control
- MAVLink communication
- Flask-based ground control interface
- Multi-drone coordination
- Independent drone IDs
- High-speed serial communication (921600 baud)
- Virtual environment deployment
- Modular and scalable architecture

---

## Hardware Requirements

### Companion Computer
- Raspberry Pi 3B
- Raspberry Pi OS (64-bit Desktop)

### Flight Controller
- Pixhawk 6X
- ArduPilot (Stable Release)

### Communication
- TELEM2 Serial Connection
- MAVLink 2
- 921600 Baud

---

## Software Stack

- Python 3.10
- DroneKit
- PyMAVLink
- MAVProxy
- Flask
- Flask-SocketIO
- Eventlet

---

# Project Structure

```
swarm/
│
├── main.py
├── config.py
├── requirements.txt
├── swarm/
│
├── templates/
├── static/
│
└── README.md
```

---

# Pixhawk Configuration

Each drone must have the following parameters configured.

| Parameter | Value |
|------------|-------|
| SERIAL2_PROTOCOL | 2 (MAVLink2) |
| SERIAL2_BAUD | 921 |
| ARMING_CHECK | 1 |
| FS_GCS_ENABLE | 1 |
| FS_EKF_ACTION | 1 |
| GUIDED_OPTIONS | 1 |

Each drone **must use a unique MAVLink System ID**.

| Drone | SYSID_THISMAV |
|---------|--------------|
| Drone 1 | 1 |
| Drone 2 | 2 |
| Drone 3 | 3 |

---

# Raspberry Pi Configuration

## Enable UART

Enable hardware UART using:

```
sudo raspi-config
```

- Disable Serial Login
- Enable Serial Hardware

Reboot afterwards.

---

## Disable Bluetooth

Edit:

```
/boot/config.txt
```

Add:

```
enable_uart=1
dtoverlay=disable-bt
```

---

## Disable Serial Console

Edit:

```
/boot/cmdline.txt
```

Remove:

```
console=serial0,115200
```

Reboot.

---

## Verify UART

```
ls -l /dev/serial0
```

Expected:

```
/dev/serial0 -> ttyAMA0
```

---

# Python Environment

Create a virtual environment.

```
python3 -m venv swarm
```

Activate:

```
source swarm/bin/activate
```

Upgrade pip.

```
pip install --upgrade pip
```

Install dependencies.

```
pip install \
dronekit \
pymavlink \
mavproxy \
future \
flask \
flask-socketio \
eventlet
```

---

# Serial Permissions

Add the user to the dialout group.

```
sudo usermod -a -G dialout $USER
```

Logout and login again.

---

# MAVLink Verification

Test communication.

```
mavproxy.py --master=/dev/serial0 --baudrate 921600
```

Expected output:

```
Heartbeat
APM: ArduCopter
GPS: 3D Fix
EKF OK
```

If successful, the Raspberry Pi is communicating correctly with the Pixhawk.

---

# Running the Swarm

Activate the environment.

```
source ~/swarm/bin/activate
```

Navigate to the project.

```
cd ~/Desktop/swarm
```

Run

```
python main.py
```

Expected output:

```
[MAV] Connecting...
[SWARM READY]
```

---

# Flask Configuration

Example drone list.

```python
DRONES = [
    "192.168.137.213",
    "192.168.137.214",
    "192.168.137.215"
]
```

Each Raspberry Pi should use its own IP address.

---

# Replicating Additional Drones

For Drone 2 and Drone 3:

1. Copy the project directory.
2. Update `config.py`.
3. Assign a unique `DRONE_ID`.
4. Ensure Pixhawk `SYSID_THISMAV` matches.
5. Verify MAVLink communication.

---

# Recommended System Configuration

Remove ModemManager to prevent serial port conflicts.

```
sudo apt purge modemmanager
sudo reboot
```

---

# Communication Architecture

```
                    Flask Ground Station
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
      ▼                    ▼                    ▼

 Raspberry Pi 1      Raspberry Pi 2      Raspberry Pi 3
      │                    │                    │
      ▼                    ▼                    ▼

 Pixhawk 1          Pixhawk 2          Pixhawk 3
      │                    │                    │
      ▼                    ▼                    ▼

    Drone 1             Drone 2             Drone 3
```

---

# Verification Checklist

- Raspberry Pi UART enabled
- Bluetooth disabled
- Serial console disabled
- `/dev/serial0` points to `ttyAMA0`
- MAVProxy installed
- MAVLink heartbeat received
- Pixhawk parameters configured
- Unique System IDs assigned
- Flask configured with drone IPs
- Swarm application launches successfully

---

# Future Improvements

- Autonomous formation control
- Dynamic swarm expansion
- Leader election
- Mesh networking
- ROS 2 integration
- Obstacle avoidance
- Mission synchronization
- Vision-based navigation

---

# License

This project is intended for educational and research purposes.
