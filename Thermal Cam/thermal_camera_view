import time
import numpy as np
import cv2
import board
import busio
import adafruit_mlx90640
from datetime import datetime

print("🚀 MLX90640 Thermal Camera + Terminal Overlay")
print("Press 's' to save screenshot | Press 'q' to quit\n")

# Initialize sensor
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ

cv2.namedWindow("MLX90640 Thermal Camera", cv2.WINDOW_NORMAL)
cv2.resizeWindow("MLX90640 Thermal Camera", 1000, 700)

screenshot_count = 0

try:
    while True:
        # Read thermal data
        frame = np.zeros((24 * 32,))
        mlx.getFrame(frame)
        temps = frame.reshape((24, 32))

        min_temp = temps.min()
        max_temp = temps.max()
        avg_temp = temps.mean()

        # === Create Visual Thermal Image ===
        if max_temp - min_temp > 0:
            normalized = ((temps - min_temp) / (max_temp - min_temp) * 255).astype(np.uint8)
        else:
            normalized = np.zeros_like(temps, dtype=np.uint8)

        resized = cv2.resize(normalized, (640, 480), interpolation=cv2.INTER_CUBIC)
        thermal_img = cv2.applyColorMap(resized, cv2.COLORMAP_JET)

        # === Overlay Information on Image ===
        overlay = thermal_img.copy()

        # Top info
        cv2.putText(overlay, f"Max: {max_temp:.1f}°C", (15, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        cv2.putText(overlay, f"Min: {min_temp:.1f}°C", (15, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        cv2.putText(overlay, f"Avg: {avg_temp:.1f}°C", (15, 105),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

        # Bottom instruction
        cv2.putText(overlay, "Press 's' = Save Screenshot | 'q' = Quit", (15, 460),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 255), 2)

        # === Show Terminal-style Temperature Array on the right side ===
        # Create a black panel on the right
        panel = np.zeros((480, 360, 3), dtype=np.uint8)

        # Add title to panel
        cv2.putText(panel, "Temperature Array (°C)", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 255, 255), 2)

        # Draw simplified 8x6 temperature grid (downsampled for readability)
        small_grid = temps[::3, ::4]   # 8 rows x 8 columns

        for i, row in enumerate(small_grid):
            for j, val in enumerate(row):
                text = f"{val:5.1f}"
                color = (0, 255, 0) if val > 30 else (255, 255, 255)
                cv2.putText(panel, text, (20 + j*42, 80 + i*45),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 1)

        # Combine thermal image + temperature panel
        combined = np.hstack((overlay, panel))

        # Show the final window
        cv2.imshow("MLX90640 Thermal Camera", combined)

        # Keyboard controls
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            screenshot_count += 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"thermal_{timestamp}_{screenshot_count:03d}.jpg"
            cv2.imwrite(filename, combined)
            print(f"✅ Screenshot saved: {filename}")

except KeyboardInterrupt:
    print("\n\n🛑 Stopped by user.")
finally:
    cv2.destroyAllWindows()
    print("Camera closed.")

