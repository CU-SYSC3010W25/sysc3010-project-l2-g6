import cv2

camera = cv2.VideoCapture(0)  # Try -1 if 0 doesn't work

if not camera.isOpened():
    print("Error: Could not open camera.")
else:
    print("Camera is working. Press 'q' to exit.")
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        cv2.imshow("Test Camera", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()
