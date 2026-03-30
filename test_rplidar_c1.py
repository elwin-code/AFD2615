import time
import numpy as np
from rplidar import RPLidar

print("🚀 Testing Slamtec RPLidar C1")
print("Make sure the sensor is connected via USB adapter\n")

# Change to /dev/ttyUSB0 if using USB adapter (most common)
# Use /dev/serial0 if doing direct UART wiring
PORT_NAME = '/dev/ttyUSB0'

try:
    lidar = RPLidar(PORT_NAME, baudrate=460800, timeout=3)   # C1 typically uses 460800

    print("✅ RPLidar connected!")
    print("Device Info:", lidar.get_info())
    print("Health:", lidar.get_health())

    print("\nStarting motor and scanning... (Press Ctrl+C to stop)\n")

    for i, scan in enumerate(lidar.iter_scans(max_buf_meas=2000)):
        print(f"Scan #{i+1} | Points: {len(scan)}")

        # Show some statistics
        distances = [distance for _, _, distance in scan if distance > 0]
        if distances:
            print(f"  → Closest: {min(distances):.1f} mm | Farthest: {max(distances):.1f} mm")

        # Optional: Print first 10 measurements (angle, distance)
        for _, angle, distance in list(scan)[:10]:
            print(f"    Angle: {angle:6.1f}° → Distance: {distance:7.1f} mm")

        print("-" * 70)

        if i > 20:   # Stop after 20 scans for testing
            break

except Exception as e:
    print(f"❌ Error: {e}")
    print("Check connection and that /dev/ttyUSB0 exists (ls /dev/ttyUSB*)")

finally:
    try:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        print("RPLidar stopped cleanly.")
    except:
        pass
