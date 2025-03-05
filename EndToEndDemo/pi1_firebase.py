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

sense = SenseHat()
firebase = pyrebase.initialize_app(config)
db = firebase.database()
dataset = "ui_test_messages"

# Write random numbers to database
def writeData():
    key = 1
    sensorData = "test pi 1"
    db.child(dataset).child(key).set(sensorData)
    time.sleep(1)
    

def readData():
  # Returns the entry as an ordered dictionary (parsed from json)
  mySensorData = db.child(dataset).get()

  print("Parent Key: {}".format(mySensorData.key()))
  print("Parent Value: {}\n".format(mySensorData.val()))

  # Returns the dictionary as a list
  mySensorData_list = mySensorData.each()
  # Takes the last element of the list
  lastDataPoint = mySensorData_list[-1]

  print("Child Key: {}".format(lastDataPoint.key()))
  print("Child Value: {}\n".format(lastDataPoint.val()))
  
#def clearData():
    #try:
        # Reference the dataset and remove all data under it
       # db.child(dataset).remove()
       # print(f"All data under '{dataset}' has been cleared.")
   # except Exception as e:
        # print(f"An error occurred while clearing data: {e}")

def main ():
   #clearData()
    writeData()
    readData()


main()

