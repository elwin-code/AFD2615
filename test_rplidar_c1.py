import time
import serial

print("🚀 RPLidar C1 - Final Simple Parser")
print("Reading raw data and attempting to extract distances...\n")

PORT = '/dev/ttyUSB0'
BAUDRATE = 460800

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print("✅ Serial opened")

    # Start scan
    ser.write(b'\xA5\x20')
    time.sleep(2)

    scan_count = 0
    print("📡 Starting scan... (one summary per second)\n")
    print("=" * 85)

    while True:
        scan_count += 1
        if ser.in_waiting > 1000:
            data = ser.read(ser.in_waiting)

            # Count how many distance values we can extract (look for reasonable distances)
            distances = []
            for i in range(len(data) - 3):
                # Look for possible distance bytes (simple heuristic for C1)
                dist = int.from_bytes(data[i:i+2], 'little')
                if 100 < dist < 12000:          # Reasonable range in mm
                    distances.append(dist / 4.0)   # Convert to mm

            valid_count = len(distances)

            if valid_count > 50:
                avg = sum(distances) / valid_count
                min_d = min(distances)
                max_d = max(distances)
                print(f"Scan #{scan_count:3d} | Valid Points: {valid_count:4d} | "
                      f"Min: {min_d:6.0f}mm | Avg: {avg:6.0f}mm | Max: {max_d:7.0f}mm")
            else:
                print(f"Scan #{scan_count:3d} | Only {valid_count} valid points - still waiting...")

        time.sleep(1.0)

except KeyboardInterrupt:
    print("\n\nStopped by user.")

except Exception as e:
    print(f"Error: {e}")

finally:
    try:
        ser.write(b'\xA5\x25')
        ser.close()
        print("RPLidar stopped.")
    except:
        pass
