import cv2
import threading

from processor import config

class Processor:
    def __init__(self):
    


        self.cap = cv2.VideoCapture(config.GST_PIPELINE, cv2.CAP_GSTREAMER)
        if not self.cap.isOpened():
            print("Error: Unable to open video stream")
            exit(-1)
        self.running = True
        self.processThread = threading.Thread(target=self.processFrames, daemon=True)
        self.processThread.start()

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def processFrames(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Unable to read frame")
                break

            # Display the frame
            cv2.imshow('Video Stream', frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                
    

