import numpy as np
import tensorflow as tf
import cv2
import mediapipe as mp

class Model:
    def __init__(self, modelPath, imgSize=64):
        self.imgSize = imgSize
        self.model = tf.keras.models.load_model(modelPath)
        self.inputShape = self.model.input_shape[1:3]  # (height, width)
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.5
        )
        
        self.class_map = {
            0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H",
            8: "I", 9: "J", 10: "K", 11: "L", 12: "M", 13: "N", 14: "O", 15: "P",
            16: "Q", 17: "R", 18: "S", 19: "T", 20: "U", 21: "V", 22: "W", 23: "X",
            24: "Y", 25: "Z", 26: "del", 27: "nothing", 28: "space"
        }

    def crop_hand(self, frame, padding=20):
        """Detects and crops hand region using MediaPipe."""
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        if results.multi_hand_landmarks:
            # Get all landmark coordinates
            landmarks = results.multi_hand_landmarks[0]
            h, w = frame.shape[:2]
            
            # Extract bounding box
            x_coords = [int(lm.x * w) for lm in landmarks.landmark]
            y_coords = [int(lm.y * h) for lm in landmarks.landmark]
            
            x_min, x_max = max(0, min(x_coords) - padding), min(w, max(x_coords) + padding)
            y_min, y_max = max(0, min(y_coords) - padding), min(h, max(y_coords) + padding)
            
            # Crop and return
            cropped = frame[y_min:y_max, x_min:x_max]
            return cropped if cropped.size != 0 else frame  # Fallback to original
        return frame  # Return original if no hand detected

    def prepareFrame(self, frame):
        """Preprocess frame with optional hand cropping."""
        # Crop hand first
        cropped_frame = self.crop_hand(frame)
        
        # Resize and normalize
        resized = cv2.resize(cropped_frame, (self.inputShape[1], self.inputShape[0]))
        return np.expand_dims(resized, axis=0) / 255.0

    def interpret(self, frame):
        inputData = self.prepareFrame(frame)
        predictions = self.model.predict(inputData, verbose=0)[0]
        classIndex = np.argmax(predictions)
        return self.class_map[classIndex], float(np.max(predictions))