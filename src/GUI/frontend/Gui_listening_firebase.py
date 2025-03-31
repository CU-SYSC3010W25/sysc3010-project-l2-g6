import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import threading
import os
import time

# Initialize Firebase
cred = credentials.Certificate("/home/divyadushy/InterprePi/sysc3010-project-l2-g6/src/GUI/sysc-3010-project-l2-g6-firebase-adminsdk-fbsvc-70fcaf4ec4.json")

# Initialize Firebase app
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com"
})

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend to communicate with backend

# Local Database
DB_FILE = "conversation.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

init_db()

# API to send a messagenew_direction
@app.route("/sendMessage", methods=["POST"])
def send_message():
    data = request.get_json()
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"success": False, "error": "Empty message"}), 400

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (content) VALUES (?)", (message,))
        conn.commit()
    return jsonify({"success": True, "message": "Message saved"}), 200

# API to get the latest message
@app.route("/latestMessage", methods=["GET"])
def get_latest_message():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM messages ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        if result:
            return jsonify({"message": result[0]})
        else:
            return jsonify({"message": "Initial Label"})
        
# Ensure "replies" table exists
def init_reply_table():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

init_reply_table()

# Route for signer to send a reply
@app.route("/sendReply", methods=["POST"])
def send_reply():
    data = request.get_json()
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"success": False, "error": "Empty reply"}), 400

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO replies (content) VALUES (?)", (message,))
        conn.commit()
    return jsonify({"success": True, "message": "Reply saved"}), 200

# Route for interpreter to get latest reply
@app.route("/latestReply", methods=["GET"])
def get_latest_reply():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM replies ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        return jsonify({"message": result[0] if result else ""})


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

# API Route to Update isSpeaking in Firebase
@app.route('/updateSpeaking', methods=['POST'])
def update_speaking():
    try:
        db.reference("settings/3").update({"isSpeaking": True})
        return jsonify({"success": True, "message": "isSpeaking updated to True"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/updateServo', methods=['POST'])
def update_servo():
    try:
        data = request.get_json()
        print("Received direction:", data)

        direction = data.get('direction')
        settings_ref = db.reference("settings/0")
        current_settings = settings_ref.get()
        print("Current Firebase settings:", current_settings)

        current_angle = current_settings.get("ServoAngle", 90)

        if direction == "up":
            #new_angle = min(current_angle + 30, 180)
            #new_direction = 1

            settings_ref.update({
                "ServoAngle": 90,
                "ServoDirection": 1
            })

            time.sleep(0.2)

        elif direction == "down":
            #new_angle = max(current_angle - 30, 0)
            #new_direction = -1

            settings_ref.update({
                "ServoAngle": 90,
                "ServoDirection": -1
            })

            time.sleep(0.2)
            
        else:
            return jsonify({"success": False, "error": "Invalid direction"}), 400

        #print("Updating Firebase to:", new_angle, new_direction)
        settings_ref.update({
            "ServoAngle": 90,
            "ServoDirection": 0
        })

        return jsonify({
            "success": True,
            "newAngle": new_angle,
            "newDirection": new_direction
        }), 200

    except Exception as e:
        print("Error in /updateServo:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)