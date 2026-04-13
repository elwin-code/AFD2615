import time
import serial
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

print("🚀 RPLidar C1 - Live Polar Plot")
print("Close the plot window or press Ctrl+C to stop\n")

PORT = '/dev/ttyUSB0'
BAUDRATE = 460800

# Create plot
plt.ion()
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='polar')
ax.set_title("RPLidar C1 - Real-time Scan", fontsize=16, pad=20)
ax.set_ylim(0, 12000)          # Max range in mm
ax.set_theta_zero_location('N')   # 0° at top
ax.set_theta_direction(-1)        # Clockwise
ax.grid(True, color='gray', alpha=0.3)

# Store latest points (for smooth updating)
points = deque(maxlen=3000)

scan_count = 0

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print("✅ Connected to RPLidar C1")

    ser.write(b'\xA5\x20')        # Start scan command
    time.sleep(2)

    print("📡 Scanning started...")

    while True:
        scan_count += 1

        if ser.in_waiting > 1000:
            data = ser.read(ser.in_waiting)

            for i in range(len(data) - 5):
                if data[i] == 0xAA and data[i+1] == 0x55:
                    try:
                        angle_raw = int.from_bytes(data[i+2:i+4], 'little')
                        dist_raw  = int.from_bytes(data[i+4:i+6], 'little')

                        angle = (angle_raw >> 1) / 64.0 * (np.pi / 180.0)   # radians
                        distance = dist_raw / 4.0

                        if 100 < distance < 12000:
                            points.append((angle, distance))
                    except:
                        pass

        # Update plot
        ax.clear()
        ax.set_ylim(0, 12000)
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.grid(True, color='gray', alpha=0.3)

        if points:
            angles, dists = zip(*points)
            ax.scatter(angles, dists, s=4, c='red', alpha=0.8)

        ax.set_title(f"RPLidar C1 Live Scan  |  Scan #{scan_count}  |  Points: {len(points)}", 
                     fontsize=14, pad=20)

        plt.pause(0.05)   # Smooth update

except KeyboardInterrupt:
    print("\n\n🛑 Stopped by user.")

except Exception as e:
    print(f"Error: {e}")

finally:
    try:
        ser.write(b'\xA5\x25')   # Stop scan
        ser.close()
        print("RPLidar stopped cleanly.")
    except:
        pass
    plt.close()
