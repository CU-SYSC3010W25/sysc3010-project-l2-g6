import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, jsonify
import time
import threading

# Path to the Firebase service account key JSON file
cred = credentials.Certificate("/home/vthanesh/sysc3010-project-l2-g6/config/interprePi access key.json")

# Initialize Firebase app
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com"
})

print("Firebase Listener Started")

app = Flask(__name__)

# Store the latest gesture
latest_gesture = {"gesture": "Initial Label"}

# Function to fetch the current value from Firebase
def get_current_gesture():
    try:
        gesture_ref = db.reference("Gestures/currentGesture")
        current_value = gesture_ref.get()
        return current_value
    except Exception as e:
        print("Error fetching current value:", str(e))
        return None

# Firebase Listener Function
def stream_listener(event):
    """Handles updates from Firebase."""
    global latest_gesture

    new_value = event.data  # The updated value from Firebase

    if new_value is None:
        print("Warning: Received None. Check Firebase for missing data.")
        return

    if new_value == latest_gesture["gesture"]:
        return  # Ignore if the gesture hasn't changed

    print("New Gesture Detected:", new_value)
    latest_gesture["gesture"] = new_value  # Update stored gesture

# Start Firebase Listener in a separate thread
def start_firebase_listener():
    stream_ref = db.reference("Gestures/currentGesture")
    stream_ref.listen(stream_listener)

# Flask Route to Get Gesture
@app.route('/gesture', methods=['GET'])
def get_gesture():
    return jsonify(latest_gesture)

# Start the Firebase listener in a separate thread
threading.Thread(target=start_firebase_listener, daemon=True).start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)