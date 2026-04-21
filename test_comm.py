#!/usr/bin/env python3
from pymavlink import mavutil
import time

print("=== Pixhawk Communication Test ===")

# Connect to Pixhawk (same as your main.py)
master = mavutil.mavlink_connection('/dev/serial0', baud=921600)

print("Waiting for heartbeat from Pixhawk...")
master.wait_heartbeat(timeout=30)

print(f"✅ SUCCESS! Connected to Pixhawk")
print(f"   System ID: {master.target_system}  Component ID: {master.target_component}")
print(f"   Autopilot: {master.autopilot}  Type: {master.type}")

# Request all sensor data
master.mav.request_data_stream_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_DATA_STREAM_ALL, 4, 1)

print("\nReceiving live data for 10 seconds...\n")

start = time.time()
while time.time() - start < 10:
    msg = master.recv_match(type=['HEARTBEAT', 'ATTITUDE', 'GLOBAL_POSITION_INT'], blocking=False)
    if msg:
        if msg.get_type() == 'ATTITUDE':
            print(f"Roll: {msg.roll:.2f}  Pitch: {msg.pitch:.2f}  Yaw: {msg.yaw:.2f}")
        elif msg.get_type() == 'GLOBAL_POSITION_INT':
            alt = msg.relative_alt / 1000.0
            print(f"Altitude: {alt:.1f} m")
    time.sleep(0.1)

print("\n✅ Communication test complete!")
