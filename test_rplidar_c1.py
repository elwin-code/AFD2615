import time
from rplidar import RPLidar, RPLidarException

print("🚀 RPLidar C1 Test - Robust Version")
print("Port: /dev/ttyUSB0 | Baudrate: 460800\n")

PORT = '/dev/ttyUSB0'

try:
    # Create lidar object with higher timeout and explicit settings
    lidar = RPLidar(PORT, baudrate=460800, timeout=5)

    print("✅ Connected to RPLidar C1")

    # Get device information
    info = lidar.get_info()
    print(f"Device Info: {info}")

    health = lidar.get_health()
    print(f"Health: {health}")

    print("\nStarting motor and scanning...")
    print("Press Ctrl+C to stop\n")

    scan_count = 0

    for scan in lidar.iter_scans(max_buf_meas=4000, min_len=50):
        scan_count += 1
        
        distances = [d for _, _, d in scan if d > 0]
        
        if distances:
            closest = min(distances)
            farthest = max(distances)
            avg_dist = sum(distances) / len(distances)
            
            print(f"Scan #{scan_count:3d} | Points: {len(scan):4d} | "
                  f"Closest: {closest:6.1f}mm | Avg: {avg_dist:6.1f}mm | "
                  f"Farthest: {farthest:7.1f}mm")
        else:
            print(f"Scan #{scan_count} → No valid measurements")

        # Force buffer clear every 5 scans (helps with C1)
        if scan_count % 5 == 0:
            try:
                lidar.clear_input()
            except:
                pass

        if scan_count >= 15:
            break

except RPLidarException as e:
    print(f"❌ RPLidar Library Error: {e}")
    print("This is common with C1. Trying recovery...")

except Exception as e:
    print(f"❌ Unexpected Error: {e}")

finally:
    try:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        print("\nRPLidar stopped cleanly.")
    except:
        pass

print("Test finished.")
