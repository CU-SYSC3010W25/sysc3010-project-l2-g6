import firebase_admin
from firebase_admin import credentials, db

#Path to the Firebase service account key JSON file
cred = credentials.Certificate("../config/interprePi access key.json")

#Initialize Firebase app (only call this ONCE per script)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://sysc-3010-project-l2-g6.firebaseio.com"
})

def stream_listener(event):
    """Callback function triggered when 'stream_enabled' changes."""
    new_value = event.data  # The new value (True/False)
    if new_value:
        print(":white_check_mark: Streaming started!")
        # Code to start RTSP server
    else:
        print(":no_entry: Streaming stopped!")
        # Code to stop RTSP server

#Attach listener to Firebase
stream_ref = db.reference("ui_test_messages/0")
stream_ref.listen(stream_listener)

