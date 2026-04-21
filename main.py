#!/usr/bin/env python3
import time
import numpy as np
from gpiozero import OutputDevice
from pymavlink import mavutil
import mlx90640
from mlx90640 import MLX90640, ChessMode
import rplidar

# ================== CONFIG ==================
RELAY_PIN = 17
BAUDRATE = 921600          # Changed to faster rate
SCAN_ALTITUDE = 15         # meters
FIRE_TEMP_THRESHOLD = 80   # °C

# ================== INIT ==================
print("🚁 Initializing Autonomous Fire Drone...")

relay = OutputDevice(RELAY_PIN, active_high=True, initial_value=False)

# Thermal Camera
thermal = MLX90640(bus=1, address=0x33, mode=ChessMode)
thermal.refresh_rate = 4

# LIDAR
lidar = rplidar.RPLidar('/dev/ttyUSB0')

# Pixhawk MAVLink
print("Connecting to Pixhawk...")
master = mavutil.mavlink_connection('/dev/serial0', baud=BAUDRATE)
master.wait_heartbeat()
print("✅ Connected to Pixhawk")

# Switch to GUIDED mode
master.mav.set_mode_send(master.target_system,
                         mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                         4)  # 4 = GUIDED in PX4

print("Switched to GUIDED mode")

def send_position_setpoint(x, y, z, yaw=0):
    """Send position command to Pixhawk"""
    master.mav.set_position_target_local_ned_send(
        0, master.target_system, master.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b110111111000,  # position only
        x, y, -z,        # NED coordinates (z is down)
        0, 0, 0,         # velocity
        0, 0, 0,         # acceleration
        yaw, 0)

# ================== MAIN LOOP ==================
def main():
    print("Starting Fire Scan Mission...")
    
    while True:
        # Read sensors
        frame, ta = thermal.get_frame(), thermal.get_ambient_temp()
        max_temp = np.max(frame)
        hot_idx = np.unravel_index(np.argmax(frame), frame.shape)
        
        # Simple fire detection
        fire_detected = max_temp > FIRE_TEMP_THRESHOLD
        
        print(f"Scan | Ta={ta:.1f}°C | Max={max_temp:.1f}°C | Fire={fire_detected}")

        if fire_detected:
            print(f"🔥 FIRE DETECTED at {hot_idx} !")
            # TODO: Fly toward hotspot (you can improve this with GPS + heading)
            trigger_retardant_drop()
        
        # Basic obstacle avoidance using LIDAR (add your logic here)
        # For now we just keep scanning
        
        time.sleep(0.25)  # 4 Hz loop

def trigger_retardant_drop(duration=3):
    print("💧 DROPPING RETARDANT!")
    relay.on()
    time.sleep(duration)
    relay.off()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMission aborted - disarming")
        relay.off()
