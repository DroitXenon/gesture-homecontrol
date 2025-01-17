import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Path to the gesture recognition model
MODEL_PATH = "models/gesture_recognizer.task"

# Mediapipe utilities for drawing
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands  # Access hand landmarks and connections

class GestureRecognizer:
    def __init__(self):
        self.recognizer = self._initialize_gesture_recognizer()

    def _initialize_gesture_recognizer(self):
        base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
        options = vision.GestureRecognizerOptions(
            base_options=base_options,
            running_mode=vision.GestureRecognizerOptions.VisionRunningMode.VIDEO
        )
        return vision.GestureRecognizer.create_from_options(options)

    def recognize_gesture(self, frame_rgb, frame_bgr):
        """
        Recognize gestures and draw landmarks on the frame.

        :param frame_rgb: The RGB frame for recognition.
        :param frame_bgr: The BGR frame for visualization.
        :return: The recognized gesture's category name or None.
        """
        try:
            # Convert the frame to MediaPipe Image format
            mp_image = vision.Image(
                image_format=vision.ImageFormat.SRGB,
                data=np.asarray(frame_rgb, dtype=np.uint8)
            )

            # Recognize gestures
            recognition_result = self.recognizer.recognize_for_video(mp_image, 0)

            # Process hand landmarks and gestures
            for idx, hand_landmarks in enumerate(recognition_result.hand_landmarks):
                # Draw landmarks on the BGR frame
                mp_drawing.draw_landmarks(
                    frame_bgr,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                )

                # Display gesture name if available
                if recognition_result.gestures[idx]:
                    gesture = recognition_result.gestures[idx][0]
                    print(f"Gesture: {gesture.category_name}, Confidence: {gesture.score:.2f}")
                    # Display the recognized gesture as text on the frame
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
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
        except Exception as e:
            print(f"Error during gesture recognition: {e}")
        return None