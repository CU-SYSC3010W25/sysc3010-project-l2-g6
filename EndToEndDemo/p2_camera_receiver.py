import cv2

# GStreamer pipeline for receiving RTP-encapsulated H.264 over UDP
gst_pipeline = (
    "udpsrc port=5000 ! "
    "application/x-rtp, media=video, encoding-name=H264, payload=96 ! "
    "rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
)

# Open the video stream in OpenCV
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

# Release everything
cap.release()
cv2.destroyAllWindows()