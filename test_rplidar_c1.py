import time
import serial

print("🚀 RPLIDAR C1 Test on Raspberry Pi 4B")
print("Motor should be spinning...\n")

PORT = '/dev/ttyUSB0'

try:
    ser = serial.Serial(PORT, 460800, timeout=1)
    print("✅ Connected to RPLIDAR C1 via USB adapter")

    # Start scanning
    ser.write(b'\xA5\x20')
    time.sleep(2)

    print("📡 Scanning started - showing one clean summary per second")
    print("=" * 80)

    scan_count = 0

    while True:
        scan_count += 1

        if ser.in_waiting > 1000:
            data = ser.read(ser.in_waiting)

            # Count how many reasonable distance values we can find
            distances = []
            for i in range(len(data) - 3):
                dist_raw = int.from_bytes(data[i:i+2], 'little')
                if 100 < dist_raw < 15000:          # Reasonable range for C1
                    distances.append(dist_raw / 4.0)   # convert to mm

            valid = len(distances)

            if valid > 30:
                avg = sum(distances) / valid
                min_d = min(distances)
                max_d = max(distances)
                print(f"Scan #{scan_count:3d} | Valid Points: {valid:4d} | "
                      f"Min: {min_d:6.0f}mm | Avg: {avg:6.0f}mm | Max: {max_d:7.0f}mm")
            else:
                print(f"Scan #{scan_count:3d} | Only {valid} valid points...")

        time.sleep(1.0)   # Slow and easy to read

except KeyboardInterrupt:
    print("\n\nStopped by user.")

finally:
    try:
        ser.write(b'\xA5\x25')   # Stop scan
        ser.close()
        print("RPLIDAR stopped cleanly.")
    except:
        pass
