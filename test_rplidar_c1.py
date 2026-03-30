import time
from rplidar import RPLidar

print("🚀 Testing Slamtec RPLidar C1")
print("Using baudrate 460800 (correct for C1)\n")

PORT_NAME = '/dev/ttyUSB0'   # Change to /dev/ttyACM0 if needed

try:
    # Important: Use 460800 baud for RPLidar C1
    lidar = RPLidar(PORT_NAME, baudrate=460800, timeout=3)

    print("✅ Connected to RPLidar C1!")
    
    # Get basic device info
    info = lidar.get_info()
    print("Device Info:", info)

    health = lidar.get_health()
    print("Health Status:", health)

    print("\nStarting motor and scanning...")
    print("Press Ctrl+C to stop\n")

    scan_count = 0
    for scan in lidar.iter_scans(max_buf_meas=3000, min_len=100):
        scan_count += 1
        distances = [d for _, _, d in scan if d > 0]

        if distances:
            closest = min(distances)
            farthest = max(distances)
            num_points = len(scan)
            
            print(f"Scan #{scan_count:3d} | Points: {num_points:4d} | "
                  f"Closest: {closest:6.1f} mm | Farthest: {farthest:7.1f} mm")

            # Show first 8 measurements for debugging
            if scan_count <= 3:
                print("   Sample angles/distances:")
                for _, angle, dist in list(scan)[:8]:
                    print(f"     {angle:6.1f}° → {dist:7.1f} mm")
        else:
            print(f"Scan #{scan_count} → No valid points")

        print("-" * 85)

        if scan_count >= 15:   # Stop after 15 scans for testing
            break

except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTroubleshooting tips:")
    print("1. Run: ls /dev/ttyUSB*   to confirm the port")
    print("2. Try: sudo chmod 666 /dev/ttyUSB0")
    print("3. Make sure the USB adapter is firmly connected")
    print("4. Try unplugging and replugging the lidar")

finally:
    try:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        print("\nRPLidar stopped cleanly.")
    except:
        pass
