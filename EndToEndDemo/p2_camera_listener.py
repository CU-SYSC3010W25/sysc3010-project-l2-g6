import subprocess
import cv2

# Define the GStreamer pipeline for receiving the video stream
gst_pipeline = (
    "udpsrc port=5000 caps=\"application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96\" ! "
    "rtph264depay ! avdec_h264 ! videoconvert ! appsink"
)

# Open the video stream using OpenCV
cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Error: Unable to open video stream")
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