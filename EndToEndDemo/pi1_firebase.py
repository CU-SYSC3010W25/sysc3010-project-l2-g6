import pyrebase
import random
import time
from sense_hat import SenseHat

# Create new Firebase config and database object
config = {
  "apiKey": "",
  "authDomain": "sysc-3010-project-l2-g6.firebaseapp.com",
  "databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com",
  "storageBucket": "lsysc-3010-project-l2-g6.firebasestorage.app"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
dataset = "ui_test_messages"

# Write random numbers to database
def writeData():
  key = 1

  data = ["Hello", "World", "From", "pi 1"]
  for i in range(4):
    db.child(dataset).child(key).set(data[i])
    time.sleep(1)

def main ():
    writeData()
main()

