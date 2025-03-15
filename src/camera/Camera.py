import os
import subprocess
import asyncio
import time
import RPi.GPIO as GPIO

from camera import config
from camera.Listener import Listener

class Camera:
    def __init__(self):
        self.listener = Listener(self.stream, self.servoUpdate)
        self.process = None
        self.running = False

        self.servoPin = None
        self.servoPWM = None
        self.servoCurrentAngle = config.SERVO_DEFAULT_ANGLE
        self.servoSpeed = 0

        self.IPScriptPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "addip.sh")
        subprocess.run(['bash', self.IPScriptPath])  # Set IP address on startup
        self.initializeServo()

    async def run(self):
        """Starts both the camera and Firebase listener asynchronously."""
        await asyncio.gather(
            self.listen_for_changes(),  # Run Firebase listener
            self.start_stream()  # Run camera stream
        )

    async def start_stream(self):
        """Manages video streaming, allowing it to be dynamically turned on/off."""
        while True:
            if self.running and self.process is None:
                print("✅ Starting Camera Stream...")
                self.process = subprocess.Popen(config.VID_CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            elif not self.running and self.process:
                print("⛔ Stopping Camera Stream...")
                self.stopCamera()

            await asyncio.sleep(1)  # Sleep briefly before rechecking

    def stopCamera(self):
        """Stops the camera stream and ensures preview is closed."""
        print("⛔ Stopping Camera Stream...")
        self.process.terminate()
        self.process.wait()  # Ensure process is fully stopped
        self.process = None

        # Kill any leftover preview windows
        subprocess.run("pkill -f libcamera-vid", shell=True)


    async def listen_for_changes(self):
        """Runs the Firebase listener asynchronously."""
        await asyncio.to_thread(self.listener.getSettings)



    #servo stuff
    def initializeServo(self):
        """Function for getting servo ready """
        self.servoPin = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servoPin, GPIO.OUT)

        self.servoPWM = GPIO.PWM(self.servoPin, 50)
        self.servoPWM.start(0)

        self.servoSpeed = 5

    def setServoAngle(self, angle):
        """
        Move servo to a specific angle, ensuring duty cycle maps to real-world servo position.
        
        Parameters:
            angle (float): The target angle in degrees. Positive values rotate clockwise,
                        negative values rotate counterclockwise, relative to the default position.
        """
        # Servo duty cycle limits (PWM percentages)
        SERVO_MIN_DUTY = 2.5  # Duty cycle for minimum angle (e.g., -90°)
        SERVO_MAX_DUTY = 12.5 # Duty cycle for maximum angle (e.g., 90°)

        # Adjust the target angle based on the default position and direction
        adjusted_angle = (angle * config.SERVO_ANGLE_AMP) + config.SERVO_DEFAULT_ANGLE

        # Clamp the adjusted angle to the servo's physical limits
        clamped_angle = max(config.SERVO_MIN_ANGLE, min(config.SERVO_MAX_ANGLE, adjusted_angle))

        # Map the clamped angle to the servo's duty cycle range
        duty_cycle = ((clamped_angle - config.SERVO_MIN_ANGLE) / 
                    (config.SERVO_MAX_ANGLE - config.SERVO_MIN_ANGLE)) * \
                    (SERVO_MAX_DUTY - SERVO_MIN_DUTY) + SERVO_MIN_DUTY

        # Apply the duty cycle to the servo
        GPIO.output(self.servoPin, True)
        self.servoPWM.ChangeDutyCycle(duty_cycle)
        time.sleep(0.2)  # Allow time for the servo to move
        GPIO.output(self.servoPin, False)
        self.servoPWM.ChangeDutyCycle(0)

        # Update the current angle and log the movement
        self.servoCurrentAngle = clamped_angle
        print(f"🔄 Servo moved to {clamped_angle}° (Requested: {angle}°) | PWM: {duty_cycle}%")


    def moveServo(self, direction):
        """move servo in a direction"""
        match direction:
            case 1:
                angle = min(self.servoCurrentAngle + self.servoSpeed, config.config.SERVO_MAX_ANGLE)
            case -1:
                angle = max(self.servoCurrentAngle - self.servoSpeed, config.config.SERVO_MIN_ANGLE)
            case _:
                return
            
        self.setServoAngle(angle)


    #callback functions
    def stream(self, enabled): 
        """Callback function to enable/disable the camera."""
        self.running = enabled
        print(f"🔥 Camera {'enabled' if enabled else 'disabled'}")

    def servoUpdate(self, key, value):
        if key == "ServoAngle":
            self.setServoAngle(value)
            print(f"Set servo angle to {value}")
        elif key == "ServoDirection":
            self.moveServo(value)