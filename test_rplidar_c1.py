import time
import serial
from datetime import datetime

print("🚀 RPLidar C1 - Reliable Test")
print("Waiting for good scans...\n")

PORT = '/dev/ttyUSB0'
BAUDRATE = 460800

ser = serial.Serial(PORT, BAUDRATE, timeout=2)

# Start scan
ser.write(b'\xA5\x20')
time.sleep(2)

scan_count = 0

try:
    while True:
        if ser.in_waiting > 100:
            data = ser.read(ser.in_waiting)
            scan_count += 1

            # Count how many valid distance measurements we can find
            valid_count = 0
            distances = []

            for i in range(len(data) - 5):
                # Look for valid measurement header (common in C1)
                if data[i] == 0xAA and data[i+1] == 0x55:
                    try:
                        angle_raw = int.from_bytes(data[i+2:i+4], 'little')
                        dist_raw = int.from_bytes(data[i+4:i+6], 'little')

                        angle = (angle_raw >> 1) / 64.0
                        distance = dist_raw / 4.0

                        if 0 < distance < 12000:   # Reasonable range for C1
                            valid_count += 1
                            distances.append(distance)
                    except:
                        pass

            # Print clean output
            if valid_count > 5:
                if distances:
                    avg_dist = sum(distances) / len(distances)
                    min_dist = min(distances)
                    max_dist = max(distances)

                    print(f"Scan #{scan_count:3d} | Valid Points: {valid_count:4d} | "
                          f"Min: {min_dist:6.0f}mm | Avg: {avg_dist:6.0f}mm | Max: {max_dist:7.0f}mm")
                else:
                    print(f"Scan #{scan_count:3d} | Valid Points: {valid_count:4d}")
            else:
                print(f"Scan #{scan_count:3d} | Only {valid_count} valid points - waiting for better data...")

            time.sleep(0.8)   # Slow and readable

except KeyboardInterrupt:
    print("\n\nStopped by user.")

finally:
    try:
        ser.write(b'\xA5\x25')  # Stop scan
        ser.close()
        print("RPLidar stopped.")
    except:
        pass
