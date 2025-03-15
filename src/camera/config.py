VID_CMD = (
    "libcamera-vid --inline --width 800 --height 600 --framerate 30 --codec h264 --bitrate 500000 -t 0 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay ! udpsink host=192.168.1.102 port=5000"
)

FB_CERT = "/home/andrewrivera/sysc3010-project-l2-g6/config/interprePi access key.json"

FB_URL = {"databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com"}

SETTINGS = "settings/0"

SERVO_DEFAULT_ANGLE = 0 #the default angle to start with 
SERVO_MIN_ANGLE = -90 #lowest the servo should be able to go down
SERVO_MAX_ANGLE = 90 #highest the servo should be able to go up
SERVO_ANGLE_AMP = -1 #multiplier for the servo angle for correction

SERVO_MIN_DUTY = 2.5  #duty cycle for minimum angle 
SERVO_MAX_DUTY = 12.5 #duty cycle for maximum angle