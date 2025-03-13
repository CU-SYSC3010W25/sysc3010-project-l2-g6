import cv2
import threading

from processor import config
from processor.Listener import Listener

class Processor:
    def __init__(self):
        self.cap = None
        self.running = False
        self.processThread = None
        self.listenerThread = None

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def createThreads(self):
        self.processThread = threading.Thread(target=self.processFrames)
        self.listenerThread = threading.Thread(target=self.stream)

    def processFrames(self):
        self.cap = cv2.VideoCapture(config.GST_PIPELINE, cv2.CAP_GSTREAMER)
        if not self.cap.isOpened():
            print("Error: Unable to open video stream")
            exit(-1)
        self.running = True
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
                
    def stream(self, enabled):
        if enabled:
            if not self.running:
                self.running = False
                self.processThread = threading.Thread(target=self.processFrames, daemon=True)
                self.processThread.start()
                print("Starting to process video")
        else:
            if self.running:
                self.running = False
                if self.processThread:
                    self.processThread.join()
                print("Stopping video processing")


