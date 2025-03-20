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

    def test_stream_is_loaded(self):
        """Test if the live stream is loaded correctly."""
        stream_element = self.wait.until(EC.presence_of_element_located((By.ID, "cameraFeed")))
        self.assertTrue(stream_element.get_attribute("src"), "Stream URL is missing")
   

if __name__ == "__main__":
    unittest.main()
