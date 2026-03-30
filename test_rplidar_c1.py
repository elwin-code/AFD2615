import time
import serial
import struct
from collections import defaultdict

print("🚀 RPLidar C1 Working Test")
print("Motor is spinning → Parsing scan data...\n")

PORT = '/dev/ttyUSB0'
BAUDRATE = 460800

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print("✅ Serial connected")

    # Start scan command
    ser.write(b'\xA5\x20')
    time.sleep(1.0)

    print("📡 Scanning... (Press Ctrl+C to stop)\n")

    scan_count = 0
    distances_by_angle = defaultdict(list)

    while True:
        if ser.in_waiting >= 2560:          # C1 typically sends ~2560 bytes per full scan
            data = ser.read(ser.in_waiting)
            scan_count += 1

            # Simple parsing for distance + angle (basic but effective)
            valid_points = 0
            min_dist = float('inf')
            max_dist = 0
            front_dist = None   # Distance in front (around 0°)

            i = 0
            while i < len(data) - 5:
                # Look for valid measurement packets (common pattern for Slamtec)
                if data[i] == 0xAA and data[i+1] == 0x55:
                    try:
                        angle_raw = struct.unpack('<H', data[i+2:i+4])[0]
                        dist_raw = struct.unpack('<H', data[i+4:i+6])[0]

                        angle = (angle_raw >> 1) / 64.0          # Convert to degrees
                        distance = dist_raw / 4.0                # Convert to mm

                        if distance > 0:
                            valid_points += 1
                            if distance < min_dist:
                                min_dist = distance
                            if distance > max_dist:
                                max_dist = distance

                            # Check front (around 0°)
                            if abs(angle) < 5 or abs(angle - 360) < 5:
                                front_dist = distance

                            distances_by_angle[int(angle)].append(distance)

                        i += 6
                    except:
                        i += 1
                else:
                    i += 1

            # Print nice summary
            print(f"    Scan #{scan_count:3d} | Valid Points: {valid_points:4d} | "
                  f"Min: {min_dist:6.0f}mm | Max: {max_dist:7.0f}mm", end="")

            if front_dist:
                print(f" | Front: {front_dist:6.0f}mm", end="")

            print()

            # Every 5 scans, show a quick summary of distances in 4 directions
            if scan_count % 20 == 0:
                print("→Summary: Front ≈ {:.0f}mm | Left ≈ {:.0f}mm | Right ≈ {:.0f}mm | Back ≈ {:.0f}mm".format(
                    distances_by_angle[0][-1] if distances_by_angle[0] else 0,
                    distances_by_angle[90][-1] if distances_by_angle[90] else 0,
                    distances_by_angle[270][-1] if distances_by_angle[270] else 0,
                    distances_by_angle[180][-1] if distances_by_angle[180] else 0
                ))
                print("-" * 90)

except KeyboardInterrupt:
    print("\n\n🛑 Stopped by user.")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    try:
        ser.write(b'\xA5\x25')   # Stop scan
        ser.close()
        print("RPLidar stopped cleanly.")
    except:
        pass
