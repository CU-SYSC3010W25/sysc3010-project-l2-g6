import cv2
from processor import config

class Processor:
    cap = None

    def __init__(self):
        self.cap = cv2.VideoCapture(config.GST_PIPELINE, cv2.CAP_GSTREAMER)
        if not self.cap.isOpened():
            print("Error: Unable to open video stream")
            exit(-1)

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def process_frames(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Unable to read frame")
                break

            # Display the frame
            cv2.imshow('Video Stream', frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break