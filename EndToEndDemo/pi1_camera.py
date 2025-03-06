import subprocess
import time

# Define the GStreamer pipeline for streaming
libcamera_vid_cmd = (
    "libcamera-vid --inline --width 800 --height 600 --framerate 30 "
    "--codec h264 --bitrate 500000 --profile baseline --inline "
    "--timeout 0 "
    "--output udp://192.168.1.102:5000"
)

# Start the GStreamer pipeline and capture errors
process = subprocess.Popen(libcamera_vid_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Keep the script alive
while True:
    time.sleep(1)
    print("Running...")
