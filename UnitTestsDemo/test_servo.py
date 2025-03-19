import RPi.GPIO as GPIO
import unittest
import time

MAX_ANGLE = 180
MIN_ANGLE = 0
DEFAULT_ANGLE = 90
SERVO_PIN = 18
MIN_DUTY = 2.5
MAX_DUTY = 12.5

def initialize_pin():
    servoPIN = 18 # GPIO 18
    return servoPIN

def minimum_duty():
    minSignal = 2.5
    return minSignal

def maximum_duty():
    maxSignal = 12.5
    return maxSignal

def initialize_servo(pin, duty):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    signal = GPIO.PWM(pin, 50) # GPIO 18 for PWM with 50Hz
    signal.start(duty) # Initialize to the minimum active pulse
    
    return signal

def set_angle(sig, angle):
    if (angle < 0):
        angle = 0
    elif (angle > 180):
        angle = 180
        
    duty = angle / 18 + 2.5
    sig.ChangeDutyCycle(duty)
    time.sleep(0.25)
    sig.ChangeDutyCycle(0)  # Turn off the signal to avoid jitter

    time.sleep(1)

    return angle
    
class TestServoFunctions(unittest.TestCase):
    def test_gpio_pin(self):
        print ("----------------------------")
        print ("-Checking GPIO PIN-")
        print ("----------------------------")

        self.assertEqual(initialize_pin(), SERVO_PIN)
        time.sleep(1)
        
        
    def test_minimum_duty(self):
        print ("----------------------------")
        print ("-Checking minimum duty value-")
        print ("----------------------------")
        self.assertEqual(minimum_duty(), MIN_DUTY)
        time.sleep(1)
        
    def test_maximum_duty(self):
        print ("----------------------------")
        print ("-Checking maximum duty value-")
        print ("----------------------------")
        self.assertEqual(maximum_duty(), MAX_DUTY)
        time.sleep(1)
        
    # Testing different angles
    def test_default(self):
        pin = initialize_pin()
        duty = minimum_duty()
        print ("----------------------------")
        print ("-Checking default angle value-")
        print ("----------------------------")
        sig = initialize_servo(pin, duty)
        
        angle = 90
        self.assertEqual(set_angle(sig, angle), DEFAULT_ANGLE)
        
    
    def test_max(self):
        pin = initialize_pin()
        duty = minimum_duty()
        print ("----------------------------")
        print ("-Checking max angle value-")
        print ("----------------------------")

        sig = initialize_servo(pin, duty)
        
        angle = 180
        self.assertEqual(set_angle(sig, angle), MAX_ANGLE)
        
    
    def test_min(self):
        pin = initialize_pin()
        duty = minimum_duty()
        sig = initialize_servo(pin, duty)
        print ("----------------------------")
        print ("-Checking min angle value-")
        print ("----------------------------")
        
        angle = 0
        self.assertEqual(set_angle(sig, angle), MIN_ANGLE)
        
        
    def test_quarter(self):
        pin = initialize_pin()
        duty = minimum_duty()
        print ("----------------------------")
        print ("-Checking 1/4 angle value-")
        print ("----------------------------")
        sig = initialize_servo(pin, duty)
        
        angle = 45
        self.assertEqual(set_angle(sig, angle), angle)
        
        
    def test_third(self):
        pin = initialize_pin()
        duty = minimum_duty()
        print ("----------------------------")
        print ("-Checking 3/4 angle value-")
        print ("----------------------------")
        sig = initialize_servo(pin, duty)
        
        angle = 135
        self.assertEqual(set_angle(sig, angle), angle)
        
    
    def test_negative(self):
        pin = initialize_pin()
        duty = minimum_duty()
        print ("----------------------------")
        print ("-Checking negative angle value-")
        print ("----------------------------")
        sig = initialize_servo(pin, duty)
        
        angle = -90
        self.assertEqual(set_angle(sig, angle), MIN_ANGLE)
        
    
    def test_out_of_range(self):
        pin = initialize_pin()
        duty = minimum_duty()
        print ("----------------------------")
        print ("-Checking out of range angle value-")
        print ("----------------------------")
        sig = initialize_servo(pin, duty)
        
        angle = 270
        self.assertEqual(set_angle(sig, angle), MAX_ANGLE)

    
    

if __name__ == '__main__':
    suite = unittest.TestSuite()

    # Run tests in the following order
    suite.addTest(TestServoFunctions('test_gpio_pin'))
    suite.addTest(TestServoFunctions('test_minimum_duty'))
    suite.addTest(TestServoFunctions('test_maximum_duty'))
    suite.addTest(TestServoFunctions('test_default'))
    suite.addTest(TestServoFunctions('test_max'))
    suite.addTest(TestServoFunctions('test_min'))
    suite.addTest(TestServoFunctions('test_quarter'))
    suite.addTest(TestServoFunctions('test_third'))
    suite.addTest(TestServoFunctions('test_negative'))
    suite.addTest(TestServoFunctions('test_out_of_range'))

    # Run the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)
