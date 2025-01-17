import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Path to the gesture recognition model
MODEL_PATH = "models/gesture_recognizer.task"

class GestureRecognizer:
    def __init__(self):
        self.recognizer = self._initialize_gesture_recognizer()

    def _initialize_gesture_recognizer(self):
        base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
        options = vision.GestureRecognizerOptions(base_options=base_options)
        return vision.GestureRecognizer.create_from_options(options)

    def recognize_gesture(self, frame_rgb):
        try:
            # Create an Image object using MediaPipe's ImageFormat and the RGB frame
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=np.asarray(frame_rgb, dtype=np.uint8)
            )
            recognition_result = self.recognizer.recognize(mp_image)

            for hand_gesture in recognition_result.gestures:
                if hand_gesture:
                    gesture = hand_gesture[0]
                    print(f"Gesture: {gesture.category_name}, Confidence: {gesture.score:.2f}")
                    return gesture.category_name
        except Exception as e:
            print(f"Error during gesture recognition: {e}")
        return None