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
UPDATE_HEARING_API = f"http://{RASPBERRY_PI_IP}:5000/updateHearing"
UPDATE_SPEAKING_API = f"http://{RASPBERRY_PI_IP}:5000/updateSpeaking"

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

    def test_speaker_button_updates_firebase(self):
        """Test if clicking the speaker button updates isHearing in Firebase."""
        button = self.wait.until(EC.element_to_be_clickable((By.ID, "speakerButton")))
        button.click()
        
        time.sleep(5)  # Allow Firebase update to propagate

        # Check Firebase for updated value
        response = requests.post(UPDATE_HEARING_API)
        self.assertEqual(response.status_code, 200, "isHearing update failed")

    def test_mic_button_updates_firebase(self):
        """Test if clicking the mic button updates isSpeaking in Firebase."""
        button = self.wait.until(EC.element_to_be_clickable((By.ID, "micButton")))
        button.click()
        
        time.sleep(5)  # Allow Firebase update to propagate

        # Check Firebase for updated value
        response = requests.post(UPDATE_SPEAKING_API)
        self.assertEqual(response.status_code, 200, "isSpeaking update failed")

if __name__ == "__main__":
    unittest.main()
