import RPi.GPIO as GPIO
import time

class Fan:
    @staticmethod
    def setupFan():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)

    @staticmethod
    def on():
        GPIO.output(18, True)

    @staticmethod
    def off():
        GPIO.output(18, False)

Fan.setupFan()
Fan.on()
time.sleep(5)
Fan.off()