import numpy as np
import tensorflow as tf
import cv2

class Model:
    def __init__(self, modelPath, imgSize=64):
        self.imgSize = imgSize
        self.model = tf.keras.models.load_model(modelPath)
        self.inputShape = self.model.input_shape[1:3]  # (height, width)
        self.class_map = {
            0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H",
            8: "I", 9: "J", 10: "K", 11: "L", 12: "M", 13: "N", 14: "O", 15: "P",
            16: "Q", 17: "R", 18: "S", 19: "T", 20: "U", 21: "V", 22: "W", 23: "X",
            24: "Y", 25: "Z", 26: "del", 27: "nothing", 28: "space"
        }

    def prepareFrame(self, frame):
        frame = cv2.resize(frame, (self.inputShape[1], self.inputShape[0]))  # Resize to model input
        frame = np.expand_dims(frame, axis=0)  # Add batch dimension
        return frame / 255.0  # Normalize to [0,1]

    def interpret(self, frame):
        inputData = self.prepareFrame(frame)
        predictions = self.model.predict(inputData, verbose=0)[0]  # Remove batch dim
        classIndex = np.argmax(predictions)
        return self.class_map[classIndex], float(np.max(predictions))  # Return (label, confidence)