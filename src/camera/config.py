VID_CMD = (
    "libcamera-vid --inline --width 800 --height 600 --framerate 30 --codec h264 --bitrate 500000 -t 0 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay ! udpsink host=192.168.1.102 port=5000"
)