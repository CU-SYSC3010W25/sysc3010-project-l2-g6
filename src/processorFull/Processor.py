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
    def __init__(self):
        self.cap = None
        self.running = False
        self.frame_queue = queue.Queue(maxsize=10)  # Buffer for frames

        self.last_stable_symbol = None
        self.current_symbol = None
        self.symbol_start_time = 0
        self.MIN_HOLD_TIME = 0.8  # Seconds to register a symbol (adjust as needed)
        self.MIN_CONFIDENCE = 0.7  # Confidence threshold (higher than print threshold)
        

        model_path = os.path.join(os.path.dirname(__file__), "model.h5")
        self.model = Model(model_path, config.IMG_SIZE)
        
        self.listener = Listener(self.stream)

        self.log_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),  # Script directory
            "predictions_log.csv"
        )
        self.init_logfile()

        self.createThreads()

    def createThreads(self):
        self.processThread = threading.Thread(target=self.processFrames)
        self.listenerThread = threading.Thread(target=self.listener.getSettings, daemon=True)
        
        self.interpretThread = threading.Thread(target=self.runInterpret, daemon=True)
        
        self.processThread.start()
        self.listenerThread.start()
        
        self.interpretThread.start()

    def init_logfile(self):
        try:
            with open(self.log_path, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "predicted_class", "confidence", "frame_time_ms"])
            print(f"✅ Log file reset: {self.log_path}")
        except Exception as e:
            print(f"❌ Failed to reset log file: {str(e)}")
            # Fallback to current directory if needed
            self.log_path = "predictions_log.csv"
            with open(self.log_path, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "predicted_class", "confidence", "frame_time_ms"])

    def processFrames(self):
        self.cap = cv2.VideoCapture(config.FFMPEG_PIPELINE, cv2.CAP_FFMPEG)
        if not self.cap.isOpened():
            print("Error: Unable to open video stream")
            return

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Unable to read frame")
                break
                
            cv2.imshow('Video Stream', frame)
            
            # Only queue frames for interpretation if not on Pi
            if self.frame_queue.qsize() < 10:
                self.frame_queue.put(frame.copy())
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False

        self.cap.release()
        cv2.destroyAllWindows()

    def runInterpret(self):
        while self.running:
            try:
                frame = self.frame_queue.get(timeout=1.0)
                start_time = time.time()
                label, confidence = self.model.interpret(frame)
                proc_time = int((time.time() - start_time)*1000)

                # Always log to CSV
                with open(self.log_path, "a", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        datetime.now().isoformat(timespec='milliseconds'),
                        label,
                        f"{confidence:.4f}",
                        proc_time
                    ])

                # Symbol hold detection logic
                current_time = time.time()
                
                if confidence < self.MIN_CONFIDENCE:
                    self.current_symbol = None  # Reset if confidence drops
                
                elif label != self.current_symbol:
                    # New symbol detected
                    self.current_symbol = label
                    self.symbol_start_time = current_time
                
                elif (current_time - self.symbol_start_time) >= self.MIN_HOLD_TIME:
                    # Symbol held long enough
                    if label != self.last_stable_symbol:
                        print(f"Letter Detected: {label} (Held {self.MIN_HOLD_TIME}s)")
                        self.last_stable_symbol = label

            except queue.Empty:
                continue

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