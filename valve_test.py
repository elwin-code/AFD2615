from gpiozero import OutputDevice
from time import sleep

# GPIO 17 controls the relay (active LOW)
relay = OutputDevice(17, active_high=False)

print("Ball Valve Test Script")
print("Commands: open, close, toggle, quit")

try:
    while True:
        cmd = input("\nEnter command (open/close/toggle/quit): ").strip().lower()
        
        if cmd == "open":
            relay.on()          # Relay activates → valve gets power
            print("✅ Valve OPEN (power ON)")
            sleep(5)            # Hold for 5 seconds (adjust for your valve)
            relay.off()         # Turn off power (valve stays in position)
            print("Valve power OFF - should stay open")
            
        elif cmd == "close":
            # For simple 2-wire valves that close when power is reversed:
            # You would need a second relay or swap polarity.
            # For this test we just turn power off (if valve is spring-return) or warn.
            relay.off()
            print("❌ Valve power OFF - check if it closes (depends on your valve)")
            sleep(3)
            
        elif cmd == "toggle":
            relay.toggle()
            state = "ON (open)" if relay.value else "OFF"
            print(f"Relay toggled → {state}")
            
        elif cmd == "quit":
            relay.off()
            print("Test ended - relay OFF")
            break
            
        else:
            print("Unknown command. Try: open, close, toggle, quit")
            
except KeyboardInterrupt:
    relay.off()
    print("\nScript stopped safely - relay turned OFF")
