#!/usr/bin/env python3
from phue import Bridge

# Replace with your bridge's IP address
BRIDGE_IP = "192.168.1.19"

def main():
    bridge = Bridge(BRIDGE_IP)
    try:
        bridge.connect()
        print(f"Connected to Hue bridge at {BRIDGE_IP}")
    except Exception as e:
        print("Error connecting to the bridge:", e)
        return

    # Get all lights as Light objects
    lights = bridge.lights

    # Print out each light’s ID and name
    print("Available lights:")
    for light in lights:
        print(f"  ID: {light.light_id}, Name: {light.name}")

if __name__ == "__main__":
    main()
