import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np


# Mediapipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_connections = mp.solutions.hands.HandLandmark

# Path to the gesture recognition model
MODEL_PATH = "models/gesture_recognizer.task"

# def classify_gesture(landmarks):
#     """
#     Classify the gesture based on hand landmarks.
#     Detects:
#     - Thumbs Up
#     - Thumbs Down
#     - Middle Finger
#     - OK Sign
#     - Fist
#     - Hand Open
#     """

def initialize_gesture_recognizer():
# 0 - Unrecognized gesture, label: Unknown
# 1 - Closed fist, label: Closed_Fist
# 2 - Open palm, label: Open_Palm
# 3 - Pointing up, label: Pointing_Up
# 4 - Thumbs down, label: Thumb_Down
# 5 - Thumbs up, label: Thumb_Up
# 6 - Victory, label: Victory
# 7 - Love, label: ILoveYou
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.GestureRecognizerOptions(base_options=base_options)
    return vision.GestureRecognizer.create_from_options(options)


def recognize_gesture_from_camera():
    
    recognizer = initialize_gesture_recognizer()
    
    camera_port = 0
    cap = cv2.VideoCapture(camera_port)

    # Error Detection
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Ignoring empty camera frame.")
                continue

            # Convert the BGR image to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Process the frame
            results = hands.process(frame_rgb)

            # Convert to MediaPipe Image format
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=np.asarray(frame_rgb, dtype=np.uint8)
            )
        
            # Gesture recognition
            try:
                recognition_result = recognizer.recognize(mp_image)
                for idx, hand_gesture in enumerate(recognition_result.gestures):
                    
                    if hand_gesture:
                        gesture = hand_gesture[0]
                        print(
                            f"Gesture: {gesture.category_name}, Confidence: {gesture.score:.2f}"
                        )

                        # Display gesture name on the frame
                        x = int(
                            recognition_result.hand_landmarks[idx][0].x * frame.shape[1]
                        )
                        y = int(
                            recognition_result.hand_landmarks[idx][0].y * frame.shape[0]
                        )
                        gesture_text = f"{gesture.category_name} ({gesture.score:.2f})"
                        cv2.putText(
                            frame,
                            gesture_text,
                            (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 255),
                            2,
                            cv2.LINE_AA,
                        )

            except Exception as e:
                print(f"Error during recognition: {e}")

            # Draw the hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )
            # Display the frame
            cv2.imshow("Hand Tracking", frame)

            # Exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_gesture_from_camera()


