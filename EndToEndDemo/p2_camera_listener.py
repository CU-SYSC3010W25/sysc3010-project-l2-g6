#receive rtsp stream from pi 1

import cv2
import time

# Updated GStreamer pipeline for receiving a raw H264 stream
gst_pipeline = (
    "udpsrc port=5000 caps=\"application/x-h264, stream-format=(string)byte-stream, alignment=(string)au\" ! "
    "h264parse ! avdec_h264 ! videoconvert ! appsink sync=false"
)

# Open the video stream using OpenCV
cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("System: Video Stream Received")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame")
        break

    # Display the frame
    cv2.imshow('Video Stream', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
