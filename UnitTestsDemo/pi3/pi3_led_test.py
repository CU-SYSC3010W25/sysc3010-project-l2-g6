import asyncio
import firebase_admin
from firebase_admin import credentials, db
from sense_hat import SenseHat
import time

# Initialize Sense HAT
sense = SenseHat()

# Initialize Firebase
cred = credentials.Certificate("../../config/interprePi access key.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com"})

latest_word = None

def display_word(word):
    """Display the word on the Sense HAT LED matrix."""
    if word:
        sense.show_message(word, scroll_speed=0.1, text_colour=[255, 255, 255], back_colour=[0, 0, 0])
        time.sleep(1)  # Pause for a second after displaying the word
        sense.clear()  # Clear the display after showing the word
    else:
        print(":warning: No word received or word is empty.")

def fetch_word(queue):
    """Listens for Firebase updates and sends them to the queue."""
    ref = db.reference("Gestures/word")

    def word_listener(event):
        """Triggered when 'Gestures/word' changes."""
        print(f"🔥 Firebase event received: {event.data}")  # Debugging line
        new_word = event.data
        queue.put_nowait(new_word)

    ref.listen(word_listener)  # Start listening in the background

async def process_updates(queue):
    """Process updates from the Firebase listener."""
    global latest_word
    while True:
        new_word = await queue.get()
        if new_word != latest_word:
            latest_word = new_word
            print(f"⚡ New Word Received: {new_word}")

            # Display the word on the Sense HAT
            display_word(new_word)

async def other_task():
    """Simulate another task running in parallel."""
    while True:
        print("🔄 Running other tasks...")
        await asyncio.sleep(5)

async def main():
    """Main async function to run Firebase listener + other tasks in parallel."""
    queue = asyncio.Queue()

    fetch_word(queue)  # Start Firebase listener in a normal function

    await asyncio.gather(
        process_updates(queue),  # Process updates from Firebase
        other_task()             # Other system task
    )

# Start the async event loop
asyncio.run(main())
