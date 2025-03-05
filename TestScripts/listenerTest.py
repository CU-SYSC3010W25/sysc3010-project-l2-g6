import asyncio
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("/home/pi/firebase-key.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://your-project-id.firebaseio.com"})

# Global variable to track latest setting (to prevent redundant processing)
latest_stream_enabled = None

async def fetch_settings(queue):
    """Background task that listens for Firebase updates and sends them to the queue."""
    ref = db.reference("settings/pi1/stream_enabled")

    def stream_listener(event):
        """Triggered when 'stream_enabled' changes."""
        new_value = event.data
        # Put the update into the queue for the asyncio event loop to process
        queue.put_nowait(new_value)

    # Run the listener in a separate thread so it doesn't block
    await asyncio.to_thread(ref.listen, stream_listener)

async def process_updates(queue):
    """Process updates from the Firebase listener."""
    global latest_stream_enabled
    while True:
        # Wait for an update from the queue
        new_value = await queue.get()
        if new_value != latest_stream_enabled:
            latest_stream_enabled = new_value
            print(f"⚡ Stream Enabled Changed: {new_value}")

            if new_value:
                print("✅ Starting RTSP Stream...")
                # Start streaming logic here
            else:
                print("⛔ Stopping RTSP Stream...")
                # Stop streaming logic here

async def other_task():
    """Simulate another task running in parallel (e.g., AI processing, RTSP streaming)."""
    while True:
        print("🔄 Running other tasks...")
        await asyncio.sleep(5)  # Simulate ongoing task

async def main():
    """Main async function to run Firebase listener + other tasks in parallel."""
    # Create a queue to communicate between the Firebase listener and the asyncio event loop
    queue = asyncio.Queue()

    # Run the Firebase listener and the update processor in parallel
    await asyncio.gather(
        fetch_settings(queue),  # Firebase listener (runs in a background thread)
        process_updates(queue),  # Process updates from Firebase
        other_task()            # Other system task (runs concurrently)
    )

# Start the async event loop
asyncio.run(main())
