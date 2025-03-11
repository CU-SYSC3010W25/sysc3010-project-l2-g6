GST_PIPELINE = (
    "udpsrc port=5000 ! "
    "application/x-rtp, media=video, encoding-name=H264, payload=96 ! "
    "rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
)