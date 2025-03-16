import numpy as np
import tflite_runtime.interpreter as tflite
import cv2

class Model:
    def __init__(self, modelPath, imgSize=64):
        self.imgSize = imgSize
        self.interpreter = tflite.Interpreter(modelPath=modelPath)
        self.interpreter.allocate_tensors()

        self.inputDetails = self.interpreter.get_input_details()
        self.outputDetails = self.interpreter.get_output_details()

    def prepareFrame(self, frame):
        frame = cv2.resize(frame, (self.imgSize, self.imgSize))
        frame = np.expand_dims(frame, axis=0) / 255.0
        return frame.astype(np.float32)
    
    def interpret(self, frame):
        inputData = self.prepareFrame(frame)
        self.interpreter.set_tensor(self.inputDetails[0]["index"], inputData)
        self.interpreter.invoke()
        outputData = self.interpreter.get_tensor(self.outputDetails[0]["index"])

        classIndex = np.argmax(outputData)
        letter = chr(classIndex + 65)
        return letter

