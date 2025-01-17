import cv2
from gesture_recognition import GestureRecognizer
from hue_control import HueController
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def process_frame_and_recognize_gesture(frame_bgr, recognition_result):
    """Process hand landmarks and gestures and return recognized gesture."""
    if recognition_result and recognition_result.hand_landmarks:
        for idx, hand_landmarks in enumerate(recognition_result.hand_landmarks):
            # Convert raw hand landmarks to drawing format
            for landmark in hand_landmarks:
                # Scale landmarks to image size for drawing
                x = int(landmark.x * frame_bgr.shape[1])
                y = int(landmark.y * frame_bgr.shape[0])
                cv2.circle(frame_bgr, (x, y), 4, (0, 255, 0), -1)

            # Draw connections manually
            for connection in mp_hands.HAND_CONNECTIONS:
                start_idx, end_idx = connection
                start = hand_landmarks[start_idx]
                end = hand_landmarks[end_idx]
                start_point = (int(start.x * frame_bgr.shape[1]), int(start.y * frame_bgr.shape[0]))
                end_point = (int(end.x * frame_bgr.shape[1]), int(end.y * frame_bgr.shape[0]))
                cv2.line(frame_bgr, start_point, end_point, (255, 0, 0), 2)

            # Display gesture name if available
            if recognition_result.gestures[idx]:
                gesture = recognition_result.gestures[idx][0]
                print(f"Gesture: {gesture.category_name}, Confidence: {gesture.score:.2f}")

                # Display the recognized gesture as text on the frame
                wrist = hand_landmarks[mp_hands.HandLandmark.WRIST]
                x, y = int(wrist.x * frame_bgr.shape[1]), int(wrist.y * frame_bgr.shape[0])
                cv2.putText(
                    frame_bgr,
                    f"{gesture.category_name} ({gesture.score:.2f})",
                    (x, y - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2,
                    cv2.LINE_AA
                )
                return gesture.category_name
    return None

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
        recognition_result = gesture_recognizer.recognizer.recognize(
            mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=frame_rgb
            )
        )

        # Process gestures and control lights
        gesture = process_frame_and_recognize_gesture(frame, recognition_result)
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
