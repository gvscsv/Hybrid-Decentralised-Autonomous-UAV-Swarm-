# safety.py

def can_fly(vehicle):
    return (
        vehicle.is_armable and
        vehicle.gps_0.fix_type >= 3 and
        vehicle.ekf_ok
    )
