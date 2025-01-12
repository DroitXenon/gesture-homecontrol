#!/usr/bin/env python3
from phue import Bridge

# Philips Hue Bridge IP
BRIDGE_IP = "192.168.1.19"

# light IDs
LIGHT_IDS = [8, 9, 10]

# The 'hue' range is 0-65535, and 'sat' range is 0-254.
# 'bri' range is 1-254. 
COLOR_MAP = {
    "red":    {"hue": 0,      "sat": 254},
    "orange": {"hue": 6000,   "sat": 254},
    "yellow": {"hue": 10000,  "sat": 254},
    "green":  {"hue": 21845,  "sat": 254},
    "blue":   {"hue": 43690,  "sat": 254},
    "purple": {"hue": 50000,  "sat": 254},
    "pink":   {"hue": 56100,  "sat": 254},
    "white":  {"hue": 0,      "sat": 0},
}

def main():
    try:
        # Connect to the bridge
        bridge = Bridge(BRIDGE_IP)
        bridge.connect()
        print(f"Connected to Hue bridge at {BRIDGE_IP}")
    except Exception as e:
        print("Error connecting to the bridge:", e)
        return

    print("Commands:")
    print("  on       -> turn all lights on at full brightness")
    print("  off      -> turn all lights off")
    print("  <color>  -> e.g. red, green, blue, white (changes color)")
    print("  quit     -> exit the script\n")

    while True:
        command = input("> ").strip().lower()

        # Turn on all lights (full brightness)
        if command == "on":
            bridge.set_light(LIGHT_IDS, 'on', True)
            bridge.set_light(LIGHT_IDS, 'bri', 254)
            print("All lights turned on at full brightness.")

        # Turn off all lights
        elif command == "off":
            bridge.set_light(LIGHT_IDS, 'on', False)
            print("All lights turned off.")

        # Change color for all lights
        elif command in COLOR_MAP:
            # Turn on lights, set brightness, hue, saturation
            color_settings = COLOR_MAP[command]
            bridge.set_light(LIGHT_IDS, 'on', True)
            # brightness too
            bridge.set_light(LIGHT_IDS, 'bri', 254)
            # hue and saturation
            bridge.set_light(LIGHT_IDS, 'hue', color_settings["hue"])
            bridge.set_light(LIGHT_IDS, 'sat', color_settings["sat"])
            print(f"All lights changed to {command}.")

        elif command == "quit":
            print("Exiting...")
            break

        else:
            print(f"Unknown command: {command}")
            print("Available commands: on, off, any color in COLOR_MAP, quit")

if __name__ == "__main__":
    main()
