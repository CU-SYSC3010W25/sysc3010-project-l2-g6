from picamera2 import Picamera2, Preview
from libcamera import Transform
import time
import subprocess

picam2 = Picamera2()
#picam2.start_preview(Preview.QTGL, x=100, y=200, width=800, height=600, transform=Transform(hflip=1))
#picam2.start()

# Define the GStreamer pipeline for streaming
libcamera_vid_cmd = (
    "libcamera-vid --inline --width 800 --height 600 --framerate 30 "
    "--codec h264 --bitrate 500000 --profile baseline --inline "
    "--output udp://192.168.1.102:5000"
)

# Start the GStreamer pipeline
subprocess.Popen(libcamera_vid_cmd, shell=True)

while (True):
    time.sleep(1)
