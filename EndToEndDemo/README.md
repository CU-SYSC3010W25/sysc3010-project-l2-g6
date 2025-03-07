The sequence of the demo goes as follows:
- p2_camera_listener.py runs to receive video stream from pi1 through ethernet connection.
- p1_camera.py runs to send encoded video stream to pi2 using the same ethernet connection.
- send_gesture.py runs to send the gesture data to the firebase continously for pi4 to read.
- pi4_listener.py runs to receive and read the data being sent and changed to the gestures variable in the firebase.
- p1_listener.py, pi2_listener.py and pi3_firebase.py are run to listen for changes to the settings variable in the firebase.
- pi4_firebase.py is then run to write to the settings variable in the firebase.

Important test files (Implemented by):
- pi1_camera.py, p1_listener (Andrew)
- p2_camera_listener (Kyle and Andrew)
