from picamera2 import Picamera2, Preview
from libcamera import Transform
import time
import subprocess

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL, x=100, y=200, width=800, height=600, transform=Transform(hflip=1))
picam2.start()

# Define the GStreamer pipeline for streaming
gst_pipeline = (
    "libcamerasrc ! video/x-raw,width=800,height=600,framerate=30/1 ! "
    "videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! "
    "rtph264pay config-interval=1 pt=96 ! "
    "udpsink host=192.168.1.102 port=5000"
)

# Start the GStreamer pipeline
subprocess.Popen(gst_pipeline, shell=True)

while (True):
    time.sleep(1)
