import RPi.GPIO as GPIO
import time



servoPIN = 18
moveUp = False
moveDown = False



GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 18 for PWM with 50Hz
p.start(2.5) # Initialization

def set_angle(angle):
    duty = angle / 18 + 2.5
    p.ChangeDutyCycle(duty)
    time.sleep(0.2)
    p.ChangeDutyCycle(0)  # Turn off the signal to avoid jitter

    return angle

try:
    current_angle = set_angle(90)
    while True:
        if (current_angle == 90):
            time.sleep(1)
        else:
            current_angle = set_angle(90)
            time.sleep(1)

except KeyboardInterrupt:
    pass
finally:
    p.stop()
    GPIO.cleanup()

