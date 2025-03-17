import cv2
import threading
import os
import subprocess
import queue

from processor import config
from processor.Listener import Listener
from processor.Model import Model

class Processor:
    def __init__(self):
        self.cap = None
        self.running = False
        self.frameQueue = queue.Queue(maxsize=1)

        self.processThread = None
        self.listenerThread = None
        self.interpretThread = None
        

        self.IPScriptPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "addip.sh")
        self.modelPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.tflite")
        self.listener = Listener(self.stream)
        self.model = Model(self.modelPath) 
        self.createThreads()    
        
        subprocess.run(['bash', self.IPScriptPath])    

    def createThreads(self):
        self.processThread = threading.Thread(target=self.processFrames)
        self.listenerThread = threading.Thread(target=self.listener.getSettings, daemon=True)
        self.interpretThread = threading.Thread(target=self.runInterpret, daemon=True)

        self.processThread.start()
        self.listenerThread.start()
        self.interpretThread.start()


    #thread functions
    def processFrames(self):
        """Process frames and stop cleanly when `self.running` is False."""
        self.cap = cv2.VideoCapture(config.GST_PIPELINE, cv2.CAP_GSTREAMER)
        if not self.cap.isOpened():
            print("Error: Unable to open video stream")
            return  # Exit safely

        while self.running:  # Process only when running is True
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Unable to read frame")
                break

            cv2.imshow('Video Stream', frame)

            if not self.frameQueue.full():
                self.frameQueue.put(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False  # Exit loop if 'q' is pressed

        # Cleanup OpenCV resources
        self.cap.release()
        cv2.destroyAllWindows()

    def runInterpret(self):
        frameCount = 0

        while self.running:
            if not self.frameQueue.get():
                frame = self.frameQueue.get()
                frameCount+= 1

                if frameCount % config.FRAME_NUM == 0:
                    letter = self.model.interpret(frame)

                    if self.checkValidChar(letter):
                        print(f"Interpreted Letter: {letter}")


    def checkValidChar(self, letter):
        return letter.isalnum() and letter.isascii()

    def stream(self, enabled):
        if enabled:
            if not self.running:
                self.running = True
                self.processThread = threading.Thread(target=self.processFrames, daemon=True)
                self.processThread.start()
                print("✅ Starting video processing")
        else:
            if self.running:
                print("⛔ Stopping video processing")
                self.running = False  # Signal the loop to stop
                if self.processThread:
                    self.processThread.join()  # Wait for the thread to finish
                    self.processThread = None  # Reset thread reference


