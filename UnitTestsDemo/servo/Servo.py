import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self):
        pass
    
    def runServo(self):
        servoPIN = 18
        moveUp = False
        moveDown = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servoPIN, GPIO.OUT)

        p = GPIO.PWM(servoPIN, 50)
        p.start(2.5)

        set_angle(90)
        time.sleep(1)

    def set_angle(angle):
        duty = angle / 18 + 2.5
        p.ChangeDutyCycle(duty)
        time.sleep(0.5)
        p.ChangeDutyCycle(0)
        p.stop()
        return angle
    