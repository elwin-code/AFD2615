import time
import board
import busio
import numpy as np
import adafruit_mlx90640

print("🚀 Testing MLX90640 with Adafruit Library...")

# Initialize I2C and sensor
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ   # 4 Hz is stable

print("✅ Sensor initialized! Starting readings...\n")
print("Press Ctrl+C to stop\n")

try:
    while True:
        frame = np.zeros((24 * 32,))          # 768 pixels
        mlx.getFrame(frame)                   # Read raw data

        temps = frame.reshape((24, 32))       # Reshape to 24x32 grid

        ta = mlx.getFrame(frame)              # Ambient is also available in some versions
        print(f"Ambient Ta ≈ {np.mean(temps):.1f}°C")
        print(f"Max Temp: {temps.max():.1f}°C")
        print(f"Min Temp: {temps.min():.1f}°C")

        # Print a small downsampled grid for easy viewing
        small = temps[::3, ::4]
        for row in small:
            print("  ".join(f"{x:5.1f}" for x in row))
        print("-" * 70)

        time.sleep(0.8)

except KeyboardInterrupt:
    print("\nTest stopped.")
