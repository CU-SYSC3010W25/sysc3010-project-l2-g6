import unittest
import servo.Servo import Servo

class TestServo(unittest.TestCase):
    def test_default_position(self):
        servo = Servo()
        self.assertEqual(servo.set_angle(90), 90)

if __name__ == '__main__':
    unittest.main()