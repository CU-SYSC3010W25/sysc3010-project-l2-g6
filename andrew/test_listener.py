import firebase_admin
from firebase_admin import credentials, db

#Path to the Firebase service account key JSON file
cred = credentials.Certificate("/home/andrewrivera/sysc3010-project-l2-g6/config/interprePi access key.json")

#Initialize Firebase app (only call this ONCE per script)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com"
})

def stream_listener(event):
    """Callback function triggered when 'stream_enabled' changes."""
    new_value = event.data  # The new value (True/False)
    if new_value:
        print(new_value)
        # Code to start RTSP server
    else:
        print("⛔ Streaming stopped!")
        # Code to stop RTSP server

#Attach listener to Firebase
stream_ref = db.reference("ui_test_messages/0")
stream_ref.listen(stream_listener) 