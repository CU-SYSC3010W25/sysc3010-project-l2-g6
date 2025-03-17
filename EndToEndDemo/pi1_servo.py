import RPi.GPIO as GPIO
import time



servoPIN = 18
moveUp = false
moveDown = false



GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 18 for PWM with 50Hz
p.start(2.5) # Initialization

def set_angle(angle):
    duty = angle / 18 + 2.5
    p.ChangeDutyCycle(duty)
    time.sleep(0.5)
    p.ChangeDutyCycle(0)  # Turn off the signal to avoid jitter

try:
    while True:
        #set_angle(0)
        #time.sleep(1)
        #set_angle(180)
        #time.sleep(1)
        set_angle(90)
        time.sleep(1)

        if (movUp){
            set_angle(180)
            moveUp = false
            time.sleep(1)
        }
        else if (moveDown){
            set_angle(0)
            moveDown = false
            time.sleep(1)
        }


except KeyboardInterrupt:
    pass
finally:
    p.stop()
    GPIO.cleanup()

