import subprocess

# Updated GStreamer pipeline for a raw H264 stream over UDP
gst_pipeline = (
    "gst-launch-1.0 udpsrc port=5000 caps=\"application/x-h264, stream-format=(string)byte-stream, alignment=(string)au\" ! "
    "h264parse ! avdec_h264 ! videoconvert ! autovideosink"
)

# Start the GStreamer pipeline
process = subprocess.Popen(gst_pipeline, shell=True)
