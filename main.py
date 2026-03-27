import time
import numpy as np
from gpiozero import OutputDevice
import mlx90640
from mlx90640 import MLX90640, ChessMode
import rplidar
import pymavlink

# ================== CONFIG ==================
RELAY_PIN = 17
REFRESH_RATE_HZ = 4

# ================== INITIALIZE ==================
print("🚀 Initializing Fire Drone System...")

# GPIO Relay for retardant drop
relay = OutputDevice(RELAY_PIN, active_high=True, initial_value=False)

# MLX90640 Thermal Camera (follows datasheet measurement flow)
thermal_sensor = MLX90640(bus=1, address=0x33, mode=ChessMode)
thermal_sensor.refresh_rate = REFRESH_RATE_HZ

# RPLIDAR (example)
lidar = rplidar.RPLidar('/dev/ttyUSB0')

# Pixhawk MAVLink (example - adjust serial port)
mav = pymavlink.MAVLinkConnection('/dev/serial0', baud=57600)

print("✅ All sensors initialized")

# ================== YOUR FUNCTIONS (from your flowchart) ==================
def initialize_sensors():
    # Already done above - EEPROM is restored automatically by the library
    pass

def read_thermal_camera():
    frame = thermal_sensor.get_frame()           # 24x32 np.array of °C
    ta = thermal_sensor.get_ambient_temp()
    return frame, ta

def detect_fire(thermal_grid, ta):
    max_temp = np.max(thermal_grid)
    hot_row, hot_col = np.unravel_index(np.argmax(thermal_grid), thermal_grid.shape)
    fire_detected = max_temp > 80  # Example threshold
    confidence = (max_temp - 60) / 100 if max_temp > 60 else 0
    return fire_detected, (hot_row, hot_col), max_temp, confidence

def trigger_retardant_drop(duration_sec=3):
    print("🔥 DROPPING RETARDANT!")
    relay.on()
    time.sleep(duration_sec)
    relay.off()
    print("✅ Drop complete")

# ================== MAIN CONTROL LOOP ==================
def main_control_loop():
    print("🔄 Starting main control loop...")
    while True:
        # 1. Read sensors
        thermal_grid, ta = read_thermal_camera()
        # lidar_scan = ... (add your lidar code here)

        # 2. Fire detection
        fire_detected, hotspot, max_temp, confidence = detect_fire(thermal_grid, ta)

        if fire_detected and confidence > 0.7:
            print(f"🔥 FIRE DETECTED! Max temp: {max_temp:.1f}°C")
            trigger_retardant_drop(3)
            # Send new waypoint to Pixhawk here
        else:
            print(f"Scanning... Ta={ta:.1f}°C  Max={np.max(thermal_grid):.1f}°C")

        time.sleep(1 / REFRESH_RATE_HZ)

if __name__ == "__main__":
    initialize_sensors()
    main_control_loop()