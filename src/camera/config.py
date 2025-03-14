VID_CMD = (
    "libcamera-vid --inline --width 800 --height 600 --framerate 30 --codec h264 --bitrate 500000 -t 0 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay ! udpsink host=192.168.1.102 port=5000"
)

FB_CERT = "/home/andrewrivera/sysc3010-project-l2-g6/config/interprePi access key.json"

FB_URL = {"databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com"}

SETTINGS = "settings/0"