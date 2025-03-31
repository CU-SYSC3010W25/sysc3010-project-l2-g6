import numpy as np
import tflite_runtime.interpreter as tflite
import cv2

class Model:
    def __init__(self, modelPath, imgSize=64):
        self.imgSize = imgSize
        self.interpreter = tflite.Interpreter(modelPath)
        self.interpreter.allocate_tensors()

        self.inputDetails = self.interpreter.get_input_details()
        self.outputDetails = self.interpreter.get_output_details()

        self.inputType = self.inputDetails[0]["dtype"]
        self.inputShape = self.inputDetails[0]["shape"]
        self.imgHeight = self.inputShape[1]
        self.imgWidth = self.inputShape[2]

    def prepareFrame(self, frame):
        frame = cv2.resize(frame, (self.imgWidth, self.imgHeight))

        if self.inputType == np.uint8: 
            frame = np.expand_dims(frame, axis=0).astype(np.uint8) 
        else:  
            frame = np.expand_dims(frame, axis=0).astype(np.float32) / 255.0

        return frame
    
    def interpret(self, frame):
        inputData = self.prepareFrame(frame)
        self.interpreter.set_tensor(self.inputDetails[0]["index"], inputData)
        self.interpreter.invoke()
        outputData = self.interpreter.get_tensor(self.outputDetails[0]["index"])

        classIndex = np.argmax(outputData)
        letter = chr(classIndex + 65)
        return classIndex

