GST_PIPELINE = (
    "udpsrc port=5000 ! "
    "application/x-rtp, media=video, encoding-name=H264, payload=96 ! "
    "rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
)

FFMPEG_PIPELINE = "udp://192.168.1.102:5000"  

FB_CERT = r"C:\Users\kylec\Programming\Code\School\SYSC3010 - Computer Systems Project\Project\sysc3010-project-l2-g6\config\interprePi access key.json"
FB_URL = {"databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com"}

SETTINGS = "settings/1"
GESTURES = "Gestures"

IMG_SIZE = 64  

SYMBOL_START_TIME = 0
MIN_HOLD_TIME = 0.5
MIN_CONFIDENCE = 0.6
