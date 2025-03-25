import unittest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Replace with your Raspberry Pi's actual IP address
RASPBERRY_PI_IP = "172.17.142.98" 
INTERPRETER_URL = f"http://{RASPBERRY_PI_IP}:8080/interpreter.html"
GESTURE_API = f"http://{RASPBERRY_PI_IP}:5000/gesture"


class TestInterpreterPage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup WebDriver for Selenium tests."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode (no browser UI)
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.get(INTERPRETER_URL)
        cls.wait = WebDriverWait(cls.driver, 10)  # 10-second timeout for waiting elements

    @classmethod
    def tearDownClass(cls):
        """Close the WebDriver after tests."""
        cls.driver.quit()


    def test_gesture_api_returns_data(self):
        """Test if the gesture API is returning data."""
        response = requests.get(GESTURE_API)
        self.assertEqual(response.status_code, 200, "Gesture API is not reachable")
        data = response.json()
        self.assertIn("gesture", data, "Gesture data is missing in API response")

    def test_camera_label_updates(self):
        """Test if cameraLabel updates with the gesture."""
        time.sleep(3)  # Increased delay to allow JS update
        label = self.wait.until(EC.presence_of_element_located((By.ID, "cameraLabel")))

        response = requests.get(GESTURE_API)
        expected_gesture = response.json().get("gesture")

        self.assertEqual(label.text, expected_gesture, "Camera label does not match currentGesture")

if __name__ == "__main__":
    unittest.main()
