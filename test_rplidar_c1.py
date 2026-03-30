import time
import asyncio
from rplidarc1 import RPLidar

print("🚀 RPLidar C1 Test using dedicated rplidarc1 library")
print("Port: /dev/ttyUSB0\n")

async def main():
    try:
        # Create lidar object
        lidar = RPLidar(port="/dev/ttyUSB0", baudrate=460800)

        print("✅ Connected to RPLidar C1!")

        # Get device info
        info = await lidar.get_info()
        print(f"Device Info: {info}")

        health = await lidar.get_health()
        print(f"Health: {health}")

        print("\nStarting continuous scan... (Press Ctrl+C to stop)\n")

        scan_count = 0
        async for scan in lidar.iter_scans():
            scan_count += 1
            distances = [d for _, _, d in scan if d > 0]

            if distances:
                closest = min(distances)
                farthest = max(distances)
                print(f"Scan #{scan_count:3d} | Points: {len(scan):4d} | "
                      f"Closest: {closest:6.1f} mm | Farthest: {farthest:7.1f} mm")
            else:
                print(f"Scan #{scan_count} → No valid points")

            if scan_count >= 20:   # Stop after 20 scans for testing
                break

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        try:
            await lidar.stop()
            print("\nRPLidar stopped cleanly.")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(main())
