import cv2
import mediapipe as mp

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_connections = mp.solutions.hands.HandLandmark

def main():
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


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


