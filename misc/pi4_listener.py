import firebase_admin
from firebase_admin import credentials, db

# Path to the Firebase service account key JSON file
cred = credentials.Certificate("sysc-3010-project-l2-g6-firebase-adminsdk-fbsvc-70fcaf4ec4.json")

# Initialize Firebase app (only call this ONCE per script)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com"
})

print("🔥 Firebase Listener Started 🔥")

# Function to fetch the current value without waiting for an event
def get_current_gesture():
    try:
        gesture_ref = db.reference("Gestures/currentGesture")
        current_value = gesture_ref.get()
        return current_value
    except Exception as e:
        print("Error fetching current value:", str(e))
        return None

# Callback function triggered when 'Gestures/currentGesture' changes
def stream_listener(event):
    """Handles updates from Firebase."""
    print(f"Event Triggered! Path: {event.path}, Data: {event.data}")
    
    new_value = event.data  # The updated value from Firebase

    if new_value is None:
        print("Warning: Received None. Check Firebase for missing data.")
        return  # Exit to avoid errors

    if not new_value:
        print("Streaming stopped!")
        # Code to stop RTSP server
    else:
        print("New Gesture Detected:", new_value)
        # Code to start RTSP server

# Attach listener to Firebase (real-time updates)
stream_ref = db.reference("Gestures/currentGesture")
stream_ref.listen(stream_listener)

# Fetch and print the current value immediately when script starts
current_gesture = get_current_gesture()
print("Initial Gesture Value:", current_gesture)

# Keep the script running
import time
while True:
    time.sleep(10)  # Prevents script from exiting
