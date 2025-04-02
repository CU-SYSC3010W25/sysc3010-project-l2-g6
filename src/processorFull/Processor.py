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
from processorFull.Streamer import StreamingHandler, StreamingOutput, StreamingServer, output


class Processor:
    def __init__(self, testing=False):
        self.testing = testing
        self.cap = None
        self.running = False
        self.frame_queue = queue.Queue(maxsize=10)
        self.streaming_server = None

        self.last_stable_symbol = None
        self.current_symbol = None
        self.symbol_start_time = config.SYMBOL_START_TIME
        self.MIN_HOLD_TIME = config.MIN_HOLD_TIME
        self.MIN_CONFIDENCE = config.MIN_CONFIDENCE
        
        self.log_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "predictions_log.csv"
        )
        model_path = os.path.join(os.path.dirname(__file__), "model.h5")

        self.model = Model(model_path, config.IMG_SIZE)
        self.listener = Listener(self.stream)
        self.init_logfile()
        self.createThreads()

    def createThreads(self):
        self.processThread = threading.Thread(target=self.processFrames)
        self.listenerThread = threading.Thread(target=self.listener.getSettings, daemon=True)
        self.interpretThread = threading.Thread(target=self.runInterpret, daemon=True)
        self.webThread = threading.Thread(target=self.start_web_server, daemon=True)
        
        self.processThread.start()
        self.listenerThread.start()
        self.interpretThread.start()
        self.webThread.start()

    def start_web_server(self):
        address = ('172.17.174.224', config.WEB_STREAM_PORT)
        self.streaming_server = StreamingServer(address, StreamingHandler)
        print(f"Web stream available at http://172.17.174.224:{config.WEB_STREAM_PORT}/")
        self.streaming_server.serve_forever()

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
            
            _, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            output.write(jpeg.tobytes())

            if self.frame_queue.qsize() < 10:
                self.frame_queue.put(frame.copy())

            if not self.testing:
                cv2.imshow('Processor Preview', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        self.cap.release()
        cv2.destroyAllWindows()

    def runInterpret(self):
        while self.running:
            try:
                frame = self.frame_queue.get(timeout=1.0)
                start_time = time.time()
                label, confidence = self.model.interpret(frame)
                proc_time = int((time.time() - start_time)*1000)

                self.log_prediction(label, confidence, proc_time)
                self.update_symbol_state(label, confidence)

            except queue.Empty:
                continue

    def update_symbol_state(self, label, confidence):
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
            self.createThreads()
            print("✅ Starting video processing")
        elif not enabled and self.running:
            print("⛔ Stopping video processing")
            self.running = False
            if self.processThread:
                self.processThread.join()
            if self.streaming_server:
                self.streaming_server.shutdown()

    def init_logfile(self):
        try:
            with open(self.log_path, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "predicted_class", "confidence", "frame_time_ms"])
        except Exception as e:
            print(f"❌ Failed to reset log file: {str(e)}")
            self.log_path = "predictions_log.csv"
            with open(self.log_path, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "predicted_class", "confidence", "frame_time_ms"])

    def log_prediction(self, label, confidence, proc_time):
        with open(self.log_path, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(timespec='milliseconds'),
                label,
                f"{confidence:.4f}",
                proc_time
            ])