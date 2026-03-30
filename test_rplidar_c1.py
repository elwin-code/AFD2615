import time
import serial
import struct
from collections import defaultdict

print("🚀 RPLidar C1 - Slow & Readable Test")
print("Motor is spinning → Showing one scan per second\n")

PORT = '/dev/ttyUSB0'
BAUDRATE = 460800

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print("✅ Serial port opened successfully\n")

    # Start scan
    ser.write(b'\xA5\x20')
    time.sleep(1.5)

    print("📡 Starting scans... (Press Ctrl+C to stop)\n")
    print("=" * 90)

    scan_count = 0

    while True:
        if ser.in_waiting >= 2000:          # Wait for a full-ish scan
            data = ser.read(ser.in_waiting)
            scan_count += 1

            valid_points = 0
            distances = []

            i = 0
            while i < len(data) - 5:
                if data[i] == 0xAA and data[i+1] == 0x55:
                    try:
                        angle_raw = struct.unpack('<H', data[i+2:i+4])[0]
                        dist_raw  = struct.unpack('<H', data[i+4:i+6])[0]

                        angle = (angle_raw >> 1) / 64.0
                        distance = dist_raw / 4.0

                        if distance > 0:
                            valid_points += 1
                            distances.append((angle, distance))
                        i += 6
                    except:
                        i += 1
                else:
                    i += 1

            # === Print nicely formatted output ===
            if distances:
                dist_values = [d for _, d in distances]
                min_dist = min(dist_values)
                max_dist = max(dist_values)
                avg_dist = sum(dist_values) / len(dist_values)

                # Find approximate cardinal directions
                front = min([d for a, d in distances if (a < 15 or a > 345)], default=0)
                left  = min([d for a, d in distances if 75 < a < 105], default=0)
                right = min([d for a, d in distances if 255 < a < 285], default=0)
                back  = min([d for a, d in distances if 165 < a < 195], default=0)

                print(f"Scan #{scan_count:3d} | Points: {valid_points:4d} | "
                      f"Min: {min_dist:6.0f}mm | Avg: {avg_dist:6.0f}mm | Max: {max_dist:7.0f}mm")

                print(f"   Front: {front:6.0f}mm | Left: {left:6.0f}mm | "
                      f"Right: {right:6.0f}mm | Back: {back:6.0f}mm")
            else:
                print(f"Scan #{scan_count:3d} → No valid points received")

            print("-" * 90)

        # Slow down the loop so it's easy to read
        time.sleep(1.0)

except KeyboardInterrupt:
    print("\n\n🛑 Stopped by user.")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    try:
        ser.write(b'\xA5\x25')   # Stop scan command
        ser.close()
        print("✅ RPLidar stopped cleanly.")
    except:
        pass
