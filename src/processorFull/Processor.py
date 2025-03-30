import cv2
import csv
import time 
from datetime import datetime
import threading
import os
import queue
import numpy as np

from processorFull import config
from processorFull.Listener import Listener
from processorFull.Model import Model

class Processor:
    def __init__(self, testing=False):
        self.testing = testing
        self.cap = None
        self.running = False
        self.frame_queue = queue.Queue(maxsize=10)  # Buffer for frames

        self.last_stable_symbol = None
        self.current_symbol = None
        self.symbol_start_time = 0
        self.MIN_HOLD_TIME = 0.8  # Seconds to register a symbol
        self.MIN_CONFIDENCE = 0.7  # Confidence threshold
        
        # Initialize model with hand cropping
        model_path = os.path.join(os.path.dirname(__file__), "model.h5")
        self.model = Model(model_path, config.IMG_SIZE)
        
        self.listener = Listener(self.stream)
        self.init_logfile()

    def processFrames(self):
        """Capture and optionally display frames with hand cropping."""
        if not self.testing:
            self.cap = cv2.VideoCapture(config.FFMPEG_PIPELINE, cv2.CAP_FFMPEG)
        else:
            self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Unable to open video stream")
            return

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Unable to read frame")
                break
                
            # Display original stream (optional)
            cv2.imshow('Video Stream', frame)
            
            # Queue frame for processing if space available
            if self.frame_queue.qsize() < 10:
                self.frame_queue.put(frame.copy())
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False

        self.cap.release()
        cv2.destroyAllWindows()

    def runInterpret(self):
        """Process frames with hand cropping and interpretation."""
        while self.running:
            try:
                frame = self.frame_queue.get(timeout=1.0)
                start_time = time.time()
                
                # Hand cropping and prediction happens here
                label, confidence = self.model.interpret(frame)
                proc_time = int((time.time() - start_time)*1000)

                # Log results
                self.log_prediction(label, confidence, proc_time)
                
                # Symbol stability logic
                self.update_symbol_state(label, confidence)

            except queue.Empty:
                continue

    def log_prediction(self, label, confidence, proc_time):
        """Log prediction to CSV."""
        with open(self.log_path, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(timespec='milliseconds'),
                label,
                f"{confidence:.4f}",
                proc_time
            ])

    def update_symbol_state(self, label, confidence):
        """Track symbol stability for Firebase updates."""
        current_time = time.time()
        
        if confidence < self.MIN_CONFIDENCE:
            self.current_symbol = None
        elif label != self.current_symbol:
            self.current_symbol = label
            self.symbol_start_time = current_time
        elif (current_time - self.symbol_start_time) >= self.MIN_HOLD_TIME:
            if label != self.last_stable_symbol:
                print(f"Letter Detected: {label} (Held {self.MIN_HOLD_TIME}s)")
                self.last_stable_symbol = label
                self.listener.updateFirebase(label)

    def stream(self, enabled):
        if enabled and not self.running:
            self.running = True
            self.processThread = threading.Thread(target=self.processFrames, daemon=True)
            self.interpretThread = threading.Thread(target=self.runInterpret, daemon=True)
            self.processThread.start()
            self.interpretThread.start()
            print("✅ Starting video processing")
        elif not enabled and self.running:
            print("⛔ Stopping video processing")
            self.running = False
            if self.processThread:
                self.processThread.join()