import os
from time import sleep

# Path for the green Activity (ACT) LED on Raspberry Pi 4B
LED_PATH = "/sys/class/leds/ACT"

# Disable default trigger (SD card activity) so we can control it manually
os.system(f"echo none | sudo tee {LED_PATH}/trigger")

print("Blinking onboard ACT LED. Press Ctrl+C to stop.")

try:
    while True:
        # Turn LED ON
        os.system(f"echo 1 | sudo tee {LED_PATH}/brightness")
        sleep(1)   # ON for 0.5 seconds

        # Turn LED OFF
        os.system(f"echo 0 | sudo tee {LED_PATH}/brightness")
        sleep(1)   # OFF for 0.5 seconds

except KeyboardInterrupt:
    # Clean up - restore default behavior when you stop the script
    os.system(f"echo mmc0 | sudo tee {LED_PATH}/trigger")
    print("\nStopped. Restored default ACT LED behavior.")
