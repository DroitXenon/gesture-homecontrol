import cv2
import mediapipe as mp

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_connections = mp.solutions.hands.HandLandmark


def classify_gesture(landmarks):
    return "None"


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
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Ignoring empty camera frame.")
                continue

            # Convert the BGR image to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb.flags.writeable = False

            # Process the frame
            results = hands.process(frame_rgb)

            # Draw the hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )

                    # Classify the gesture
                    print(classify_gesture(hand_landmarks.landmark))

            # Display the frame
            cv2.imshow("Hand Tracking", frame)

            # Exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


