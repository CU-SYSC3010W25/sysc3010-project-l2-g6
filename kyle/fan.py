import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

class Fan:
    @staticmethod
    def on():
        GPIO.output(18, True)

    @staticmethod
    def off():
        GPIO.output(18, False)