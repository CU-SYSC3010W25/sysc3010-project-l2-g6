import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

class TestModel:
    def __init__(self, images_name: str, model_name: str):
        # Get absolute paths to the images folder and model file
        self.images_dir = os.path.join(os.path.dirname(__file__), images_name)
        self.model_path = os.path.join(os.path.dirname(__file__), model_name)

        # Load the model
        self.model = tf.keras.models.load_model(self.model_path)

    def run_tests(self):
        # List of expected classes (A-Z, nothing, space, del)
        expected_classes = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ['nothing', 'space', 'del']

        # Track test results
        total_tests = 0
        passed_tests = 0

        # Iterate through each image in the images folder
        for filename in os.listdir(self.images_dir):
            # Construct full path to the image
            img_path = os.path.join(self.images_dir, filename)

            # Skip if it's not a file (e.g., subdirectories)
            if not os.path.isfile(img_path):
                continue

            # Extract the expected class from the filename
            # Assumes filenames are in the format: <class>_<rest>.jpg
            expected_class = filename.split(".jpg")[0]

            # Skip if the expected class is not in the list of valid classes
            if expected_class not in expected_classes:
                print(f"Skipping file '{filename}' (unknown class '{expected_class}')")
                continue

            # Load and preprocess the image
            img = image.load_img(img_path, target_size=(64, 64))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            img_array = img_array / 255.0  # Normalize to [0, 1]

            # Run prediction
            predictions = self.model.predict(img_array)
            predicted_class_index = np.argmax(predictions, axis=1)[0]
            predicted_class = expected_classes[predicted_class_index]

            # Check if the prediction matches the expected class
            total_tests += 1
            if predicted_class == expected_class:
                passed_tests += 1
                print(f"Test {total_tests}: Correctly predicted '{filename}' as '{predicted_class}'")
            else:
                print(f"Test {total_tests}: Incorrectly predicted '{filename}' as '{predicted_class}' (expected '{expected_class}')")

        # Print summary
        print(f"\nTest Summary:")
        print(f"Total tests: {total_tests}")
        print(f"Passed tests: {passed_tests}")
        print(f"Accuracy: {(passed_tests / total_tests) * 100:.2f}%")

# Example usage
if __name__ == "__main__":
    # Initialize the tester
    tester = TestModel(images_name="images", model_name="model.h5")

    # Run the tests
    tester.run_tests()