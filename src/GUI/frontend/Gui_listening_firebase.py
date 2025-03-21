from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import threading

# Initialize Firebase
cred = credentials.Certificate("/home/divyadushy/InterprePi/sysc3010-project-l2-g6/config/interprePi access key.json")

# Initialize Firebase app
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com"
})

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend to communicate with backend

# Store latest gesture
latest_gesture = {"gesture": "Initial Label"}

# Firebase Listener Function (Listens for changes in currentGesture)
def stream_listener(event):
    global latest_gesture
    new_value = event.data
    if new_value is not None:
        latest_gesture["gesture"] = new_value
        print("Updated Gesture:", new_value)

# Start Firebase listener in a separate thread
def start_firebase_listener():
    gesture_ref = db.reference("Gestures/currentGesture")
    gesture_ref.listen(stream_listener)

# Start the Firebase listener thread
threading.Thread(target=start_firebase_listener, daemon=True).start()

# API Route to Get Latest Gesture
@app.route('/gesture', methods=['GET'])
def get_gesture():
    return jsonify(latest_gesture)

# API Route to Update isHearing in Firebase
@app.route('/updateHearing', methods=['POST'])
def update_hearing():
    try:
        db.reference("settings/3").update({"isHearing": True})
        return jsonify({"success": True, "message": "isHearing updated to True"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# API Route to Update isHearing in Firebase
@app.route('/updateSpeaking', methods=['POST'])
def update_speaking():
    try:
        db.reference("settings/3").update({"isSpeaking": True})
        return jsonify({"success": True, "message": "isHearing updated to True"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)