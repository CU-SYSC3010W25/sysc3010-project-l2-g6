import firebase_admin
from firebase_admin import credentials, db
from multiprocessing import Process, Manager
import time

# Initialize Firebase
cred = credentials.Certificate("sysc-3010-project-l2-g6-firebase-adminsdk-fbsvc-70fcaf4ec4.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com"})

def run_listener(shared_state):
    """Runs the Firebase listener and updates the shared state."""
    ref = db.reference("ui_test_messages/0")

    def stream_listener(event):
        """Triggered when 'stream_enabled' changes."""
        new_value = event.data
        print(f"🔥 Firebase Listener: Stream Enabled Changed to {new_value}")
        shared_state["value"] = bool(new_value)  # Convert to boolean

    # Start the Firebase listener (blocking call)
    ref.listen(stream_listener)

def main_app(shared_state):
    """Reads the shared state and acts on it."""
    while True:
        current_state = shared_state["value"]
        print(f"🔄 Main App: Current Stream Enabled State = {current_state}")

        if current_state:
            print("✅ Main App: Starting RTSP Stream...")
            # Start RTSP streaming logic here
        else:
            print("⛔ Main App: Stopping RTSP Stream...")
            # Stop RTSP streaming logic here

        time.sleep(5)  # Simulate ongoing task

if __name__ == "__main__":
    # Use Manager dict to share data across processes
    with Manager() as manager:
        shared_state = manager.dict()
        shared_state["value"] = False  # Default to False

        # Start Firebase listener process
        listener_process = Process(target=run_listener, args=(shared_state,))
        listener_process.start()

        # Start main application process
        app_process = Process(target=main_app, args=(shared_state,))
        app_process.start()

        # Keep both processes running
        listener_process.join()
        app_process.join()
