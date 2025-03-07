import firebase_admin
from firebase_admin import credentials, db
import time

# Path to the Firebase service account key JSON file
cred = credentials.Certificate("/home/divyadushy/InterprePi/sysc3010-project-l2-g6/config/interprePi access key.json")

# Initialize Firebase app (only call this ONCE per script)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com"
})

print("Firebase Listener Started")

# Function to fetch the current value without waiting for an event
def get_current_gesture():
    try:
        gesture_ref = db.reference("Gestures/currentGesture")
        current_value = gesture_ref.get()
        return current_value
    except Exception as e:
        print("Error fetching current value:", str(e))
        return None

# Get initial value before starting the listener
previous_gesture = get_current_gesture()
print("Current Gesture Value:", previous_gesture)

# Callback function triggered when 'Gestures/currentGesture' changes
def stream_listener(event):
    """Handles updates from Firebase."""
    global previous_gesture  # Store last known value

    new_value = event.data  # The updated value from Firebase

    if new_value is None:
        print("Warning: Received None. Check Firebase for missing data.")
        return  # Exit to avoid errors

    if new_value == previous_gesture:
        return  # Ignore if the gesture hasn't changed

    if not new_value:  # No gesture detected
        print("Streaming stopped!")
        # Code to stop RTSP server
    else:
        print("New Gesture Detected:", new_value)
        # Code to start RTSP server

    previous_gesture = new_value  # Update the stored gesture

# Attach listener to Firebase (real-time updates)
stream_ref = db.reference("Gestures/currentGesture")
stream_ref.listen(stream_listener)

# Keep the script running
while True:
    time.sleep(10)  # Prevents script from exiting
