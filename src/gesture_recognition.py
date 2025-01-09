import cv2
import mediapipe as mp

def main():
    camera_port = 0
    cap = cv2.VideoCapture(camera_port)


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


