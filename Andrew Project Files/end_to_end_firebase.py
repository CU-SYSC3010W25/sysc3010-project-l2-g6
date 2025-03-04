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
dataset = "andrew_sensor"

# Write random numbers to database
def writeData():
    key = 0

    for i in range (3):
        sensorData = sense.get_temperature()

        # Will be written in this form:
        # {
        #   "andrew_sensor" : {
    #     "0" : 0.6336863763908736,
    #     "1" : 0.33321038818190285,
    #     "2" : 0.6069185320998802,
    #     "3" : 0.470459178006184,
    #   }
    # }
    # Each 'child' is a JSON key:value pair
        db.child(dataset).child(key).set(sensorData)

        key = key + 1
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
  
def clearData():
    try:
        # Reference the dataset and remove all data under it
        db.child(dataset).remove()
        print(f"All data under '{dataset}' has been cleared.")
    except Exception as e:
        print(f"An error occurred while clearing data: {e}")

def main ():
    clearData()
    writeData()
    readData()


main()

