#listen for settings update from firebase

import asyncio
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("/home/kylemathias/Project/sysc3010-project-l2-g6/config/interprePi access key.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com"})

latest_stream_enabled = None

def fetch_settings(queue):
    """Listens for Firebase updates and sends them to the queue."""
    ref = db.reference("settings/1")

    def stream_listener(event):
        """Triggered when 'stream_enabled' changes."""
        print(f"🔥 Firebase event received: {event}")  # Debugging line
        new_value = event.data
        queue.put_nowait(new_value)

    ref.listen(stream_listener)  # Start listening in the background

async def process_updates(queue):
    """Process updates from the Firebase listener."""
    global latest_stream_enabled
    while True:
        new_value = await queue.get()
        if new_value != latest_stream_enabled:
            latest_stream_enabled = new_value
            print(f"⚡ Stream Enabled Changed: {new_value}")

            if new_value:
                print("✅ Starting RTSP Stream...")
            else:
                print("⛔ Stopping RTSP Stream...")

async def other_task():
    """Simulate another task running in parallel."""
    while True:
        print("🔄 Running other tasks...")
        await asyncio.sleep(5)

async def main():
    """Main async function to run Firebase listener + other tasks in parallel."""
    queue = asyncio.Queue()

    fetch_settings(queue)  # Start Firebase listener in a normal function

    await asyncio.gather(
        process_updates(queue),  # Process updates from Firebase
        other_task()             # Other system task
    )

# Start the async event loop
asyncio.run(main())

