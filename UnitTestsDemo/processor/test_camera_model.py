import os
import tensorflow as tf
import numpy as np
import cv2
import time

"""
Class indices: {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 
'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 
'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25, 
'del': 26, 'nothing': 27, 'space': 28}
"""

class LiveCameraTest:
    def __init__(self, model_name: str):
        # Get absolute path to the model file
        self.model_path = os.path.join(os.path.dirname(__file__), model_name)

        # Load the model
        self.model = tf.keras.models.load_model(self.model_path)

        # List of expected classes (A-Z, nothing, space, del)
        self.expected_classes = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ['del', 'nothing', 'space']

    def run_live_test(self):
        # Open the camera
        cap = cv2.VideoCapture(0)  # 0 is the default camera

        if not cap.isOpened():
            print("Error: Could not open camera.")
            return

        # Initialize timer
        last_prediction_time = time.time()

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            if not ret:
                print("Error: Could not read frame.")
                break

            # Display the frame
            cv2.imshow("Live Camera Feed", frame)

            # Check if 5 seconds have passed since the last prediction
            current_time = time.time()
            if current_time - last_prediction_time >= 5:
                # Preprocess the frame for prediction
                resized_frame = cv2.resize(frame, (64, 64))  # Resize to 64x64
                img_array = np.array(resized_frame, dtype=np.float32)  # Convert to float32
                img_array = img_array / 255.0  # Normalize to [0, 1]
                img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

                # Run prediction
                predictions = self.model.predict(img_array)
                predicted_class_index = np.argmax(predictions, axis=1)[0]
                predicted_class = self.expected_classes[predicted_class_index]

                # Print the predicted class
                print(f"Predicted class: {predicted_class}")

                # Update the last prediction time
                last_prediction_time = current_time

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close the window
        cap.release()
        cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    # Initialize the tester
    tester = LiveCameraTest(model_name="model.h5")

    # Run the live camera test
    tester.run_live_test()