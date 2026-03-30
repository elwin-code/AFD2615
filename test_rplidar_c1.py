import time
import serial

print("🚀 RPLidar C1 - Basic Reliable Test")
print("This version reads raw data slowly for debugging\n")

PORT = '/dev/ttyUSB0'
BAUDRATE = 460800

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print("✅ Serial port opened")

    # Start the scan
    ser.write(b'\xA5\x20')
    time.sleep(2)

    print("📡 Reading raw data... (one update per second)\n")
    print("=" * 80)

    scan_count = 0

    while True:
        scan_count += 1
        if ser.in_waiting > 0:
            data = ser.read(min(ser.in_waiting, 4096))   # Read up to 4KB
            byte_count = len(data)

            print(f"Scan #{scan_count:3d} | Received {byte_count:4d} bytes")

            # Count how many potential measurement packets we see
            packet_count = 0
            for i in range(len(data) - 1):
                if data[i] == 0xAA and data[i+1] == 0x55:
                    packet_count += 1

            print(f"   → Found {packet_count} potential measurement packets")

            if byte_count > 1000:
                print("   → Good data volume! Sensor is transmitting properly.")
            elif byte_count > 100:
                print("   → Partial data received.")
            else:
                print("   → Very little data.")

        else:
            print(f"Scan #{scan_count:3d} | No data waiting...")

        print("-" * 80)
        time.sleep(1.0)   # Slow and easy to read

except KeyboardInterrupt:
    print("\n\n🛑 Stopped by user.")

finally:
    try:
        ser.write(b'\xA5\x25')  # Stop scan
        ser.close()
        print("Port closed.")
    except:
        pass
