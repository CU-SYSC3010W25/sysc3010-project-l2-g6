import subprocess

# Define the GStreamer pipeline for receiving and displaying the video stream
gst_pipeline = (
    "gst-launch-1.0 udpsrc port=5000 caps=\"application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96\" ! "
    "rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink"
)

# Start the GStreamer pipeline
subprocess.Popen(gst_pipeline, shell=True)