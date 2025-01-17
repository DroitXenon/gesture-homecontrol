from gesture_recognition import GestureRecognizer
from hue_control import HueController
import cv2

def main():
    # Initialize gesture recognizer and Hue controller
    gesture_recognizer = GestureRecognizer()
    hue_controller = HueController()

    # Set up the camera
    camera_port = 1
    cap = cv2.VideoCapture(camera_port)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Press 'q' to quit.")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Ignoring empty camera frame.")
            continue

        # Convert the BGR image to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Recognize gestures
        gesture = gesture_recognizer.recognize_gesture(frame_rgb)

        # Control lights based on gestures
        if gesture == "Thumb_Up":
            hue_controller.turn_on_lights()
        elif gesture == "Thumb_Down":
            hue_controller.turn_off_lights()

        # Display the frame
        cv2.imshow("Gesture Recognition", frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()