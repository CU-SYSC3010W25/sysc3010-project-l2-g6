import firebase_admin
from firebase_admin import credentials, db
from multiprocessing import Process, Value

# Initialize Firebase
cred = credentials.Certificate("/home/pi/firebase-key.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://your-project-id.firebaseio.com"})

def run_listener(shared_state):
    """Runs the Firebase listener and updates the shared state."""
    ref = db.reference("settings/pi1/stream_enabled")

    def stream_listener(event):
        """Triggered when 'stream_enabled' changes."""
        new_value = event.data
        print(f"⚡ Firebase Listener: Stream Enabled Changed to {new_value}")
        shared_state.value = new_value  # Update the shared state

    # Start the Firebase listener (blocking call)
    ref.listen(stream_listener)

if __name__ == "__main__":
    # Create a shared variable to store the state
    shared_state = Value('i', 0)  # 'i' for integer, initial value 0

    # Start the Firebase listener in a separate process
    listener_process = Process(target=run_listener, args=(shared_state,))
    listener_process.start()

    # Keep the listener process running
    listener_process.join()
