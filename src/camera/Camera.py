import os
import subprocess
import asyncio
import time
import RPi.GPIO as GPIO

from camera import config
from camera.Listener import Listener

class Camera:
    def __init__(self):
        self.listener = Listener(self.stream, self.servoUpdate) #listener for firebase updates
        self.process = None #subprocess child program object for the video stream
        self.running = False #controls when the camera can send stream

        self.servoPin = None #GPIO pin for the servo motor
        self.servoPWM = None #PWM for the servo motor
        self.servoCurrentAngle = config.SERVO_DEFAULT_ANGLE #set the current servo angle to the specified default
        self.servoSpeed = 0 #number of degrees to move the servo each period
        self.servoDirection = 0 #direction that the servo is moving in

        self.IPScriptPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "addip.sh") #get path of add ethernet ip script
        subprocess.run(['bash', self.IPScriptPath])  #run the add ethernet ip script
        self.initializeServo() #initialize servo values


    #asynchronous functions
    async def run(self): #start all async functions to run asynchronously
        await asyncio.gather(
            self.settingsListen(),  #run firebase listener
            self.startStream(),  #run camera stream
            self.servoMovement() #run servo motor 
        )

    async def startStream(self): #function to turn video stream on and off
        while True:
            if self.running and self.process is None: #if running but theres no process then create one with the video stream
                print("Starting Camera Stream.")
                self.process = subprocess.Popen(config.VID_CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            elif not self.running and self.process: #if not running and the process exists then close the process
                print("Stopping Camera Stream.")
                self.stopCamera() #function to terminate process

            await asyncio.sleep(1)  #sleep

    async def settingsListen(self): #start settings listener
        await asyncio.to_thread(self.listener.getSettings) #call the listener to start getting settings

    async def servoMovement(self): #move servo continuously in a direction until min/max value hit
        while True: #only enter block if the servo direction isnt 0 and the angle is within the min and max in that direction
            if self.servoDirection != 0 or (self.servoDirection == 1 and angle <= config.SERVO_MAX_ANGLE) or (self.servoDirection == -1 and angle >= config.SERVO_MIN_ANGLE):
                angle = self.servoCurrentAngle + (self.servoDirection * self.servoSpeed) #calculate the angle
                
                #set the angle adjustment as long as its within the limits
                if self.servoDirection == 1 and angle <= config.SERVO_MAX_ANGLE:
                    self.setServoAngle(angle * config.SERVO_ANGLE_AMP)
                elif self.servoDirection == -1 and angle >= config.SERVO_MIN_ANGLE:
                    self.setServoAngle(angle * config.SERVO_ANGLE_AMP)
                
                await asyncio.sleep(1) #sleep
            
            await asyncio.sleep(0.1) #sleep



    #camera functions
    def stopCamera(self): #stop the camera stream
        self.process.terminate() #kill the process
        self.process.wait()  #wait for the process to die
        self.process = None #set process reference to none

        subprocess.run("pkill -f libcamera-vid", shell=True) #clean up any preview windows



    #servo stuff
    def initializeServo(self): #initializes servo values
        self.servoPin = config.SERVO_GPIO_PIN #set servo GPIO pin
        GPIO.setmode(GPIO.BCM) #set servo mode to BCM
        GPIO.setup(self.servoPin, GPIO.OUT) #set GPIO pin 18 as an output pin

        self.servoPWM = GPIO.PWM(self.servoPin, config.SERVO_FREQ) #set the pulse width modulation with the frequency for pin 18
        self.servoPWM.start(0) #start the PWM

        self.servoSpeed = config.SERVO_SPEED #set the servo speed

    def setServoAngle(self, angle: float): #moves the servo to an angle within the min and max limits
        adjusted_angle = (angle * config.SERVO_ANGLE_AMP) + config.SERVO_DEFAULT_ANGLE #adjust the angle using the offset and amplifier
        clamped_angle = max(config.SERVO_MIN_ANGLE, min(config.SERVO_MAX_ANGLE, adjusted_angle)) #make sure the angle stays within the limits
        duty_cycle = ((clamped_angle - config.SERVO_MIN_ANGLE) / 
                    (config.SERVO_MAX_ANGLE - config.SERVO_MIN_ANGLE)) * \
                    (config.SERVO_MAX_DUTY - config.SERVO_MIN_DUTY) + config.SERVO_MIN_DUTY #calculate the duty cycle of the angle

        #apply duty cycle to the servo to move
        GPIO.output(self.servoPin, True)
        self.servoPWM.ChangeDutyCycle(duty_cycle)
        time.sleep(0.2) 
        GPIO.output(self.servoPin, False)
        self.servoPWM.ChangeDutyCycle(0)

        #update the internal current angle
        self.servoCurrentAngle = clamped_angle
        print(f"Servo moved to {clamped_angle}°")

    def moveServo(self, direction): #function to continuously move the servo in a direction
        print(f"Servo direction changed to {direction}")
        self.servoDirection = direction



    #callback functions
    def stream(self, enabled: bool): #callback function for when the stream setting is changed 
        self.running = enabled #set running whether true or false
        print(f"Camera {'enabled' if enabled else 'disabled'}")

    def servoUpdate(self, key: str, value: float): #callback function for when one of the servo settings is changed
        if key == "ServoAngle": #if its a hard set then call setServoAngle
            self.setServoAngle(value)
            print(f"Set servo angle to {value}")
        elif key == "ServoDirection": #if its a direction then call moveServo
            self.moveServo(value)


    

