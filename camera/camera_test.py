import cv2

active_ports = [0]  # Update based on your output

for port in active_ports:
    print(f"Testing /dev/video{port}...")
    cap = cv2.VideoCapture(port)
    if cap.isOpened():
        print(f"Camera working on port: /dev/video{port}. Press 'q' to quit the preview.")
        while True:
            ret, frame = cap.read()
            if not ret:
                print(f"Failed to capture on port: /dev/video{port}")
                break
            cv2.imshow(f"Camera - /dev/video{port}", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print(f"No feed from /dev/video{port}.")