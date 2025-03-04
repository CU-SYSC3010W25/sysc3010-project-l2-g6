from picamera2 import Picamera2
from time import sleep

cam = Picamera2()
cam.start_preview()
# Keep the preview window open for 5 seconds
sleep(5)
cam.stop_preview()