import cv2

def find_active_camera_ports(max_ports):
    """
    Check which video ports are active (accessible) for cameras.
    :param max_ports: The maximum number of video ports to check.
    :return: A list of active camera ports.
    """
    active_ports = []
    for port in range(max_ports):
        cap = cv2.VideoCapture(port)
        if cap.isOpened():
            print(f"Camera found on port: /dev/video{port}")
            active_ports.append(port)
            cap.release()
        else:
            print(f"No camera on port: /dev/video{port}")
    return active_ports

if __name__ == "__main__":
    print("Scanning for active camera ports...")
    active_ports = find_active_camera_ports(max_ports=40)  # Adjust max_ports if you have more devices
    if active_ports:
        print(f"Active camera ports: {active_ports}")
    else:
        print("No active cameras detected.")