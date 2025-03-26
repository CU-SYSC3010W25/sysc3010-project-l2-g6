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

    def test_page_is_accessible(self):
        """Test if the interpreter page is accessible."""
        response = requests.get(INTERPRETER_URL)
        self.assertEqual(response.status_code, 200, "Interpreter page is not accessible")


if __name__ == "__main__":
    unittest.main()
