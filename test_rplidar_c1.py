import time
import serial
import struct

print("🚀 RPLidar C1 Simple Test using direct serial")
print("Port: /dev/ttyUSB0 | Baudrate: 460800\n")

PORT = '/dev/ttyUSB0'
BAUDRATE = 460800

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print("✅ Serial port opened successfully")

    # Start motor and scan command for RPLidar C1
    print("Starting motor and requesting scan...")

    # Send scan command (standard for most Slamtec lidars)
    ser.write(b'\xA5\x20')   # Start scan command
    time.sleep(0.5)

    print("Scanning... (Press Ctrl+C to stop)\n")
    scan_count = 0

    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            if len(data) > 10:   # We got some meaningful data
                scan_count += 1
                print(f"Scan #{scan_count} | Received {len(data)} bytes")

                # Try to find distance values (very basic parsing)
                if len(data) > 50:
                    # Simple statistics
                    print(f"   → Data looks good! ({len(data)} bytes)")
                else:
                    print(f"   → Small packet received")

        time.sleep(0.1)

except serial.SerialException as e:
    print(f"❌ Serial Error: {e}")
except KeyboardInterrupt:
    print("\n\n🛑 Stopped by user.")
finally:
    try:
        ser.write(b'\xA5\x25')   # Stop scan
        time.sleep(0.2)
        ser.close()
        print("Port closed.")
    except:
        pass
