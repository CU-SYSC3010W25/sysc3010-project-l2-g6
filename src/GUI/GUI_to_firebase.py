import pyrebase
import time

# Firebase Config
config = {
  "apiKey": "",
  "authDomain": "sysc-3010-project-l2-g6.firebaseapp.com",
  "databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com",
  "storageBucket": "sysc-3010-project-l2-g6.firebasestorage.app"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
dataset = "ui_test_messages"

# Write test messages to Firebase
def writeTestMessages():
    messages = ["Hello World!", "Testing 1", "This is a UI test"]
   
    for i, msg in enumerate(messages):
        db.child(dataset).child(i).set(msg)
        time.sleep(1)

    print("Test messages written to Firebase.")

# Read messages back from Firebase
def readTestMessages():
    myMessages = db.child(dataset).get()

    print("Messages from Firebase:")
    for message in myMessages.each():
        print(f"{message.key()}: {message.val()}")

# Clear previous test messages
def clearTestMessages():
    try:
        db.child(dataset).remove()
        print(f"All messages under '{dataset}' have been cleared.")
    except Exception as e:
        print(f"Error clearing messages: {e}")

def main():
    clearTestMessages()
    writeTestMessages()
    readTestMessages()

main()
