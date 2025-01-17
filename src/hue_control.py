from phue import Bridge

# Philips Hue Bridge IP
BRIDGE_IP = "192.168.1.19"
# Light IDs to control
LIGHT_IDS = [8, 9, 10]

class HueController:
    def __init__(self, bridge_ip=BRIDGE_IP):
        try:
            self.bridge = Bridge(bridge_ip)
            self.bridge.connect()
            print(f"Connected to Hue bridge at {bridge_ip}")
        except Exception as e:
            print("Error connecting to the bridge:", e)
            self.bridge = None

    def turn_on_lights(self):
        if self.bridge:
            self.bridge.set_light(LIGHT_IDS, 'on', True)
            self.bridge.set_light(LIGHT_IDS, 'bri', 254)
            print("Lights turned ON.")

    def turn_off_lights(self):
        if self.bridge:
            self.bridge.set_light(LIGHT_IDS, 'on', False)
            print("Lights turned OFF.")
