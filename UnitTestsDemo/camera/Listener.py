import firebase_admin
from firebase_admin import credentials, db

from camera import config

class Listener:
    def __init__(self, streamCallback, servoCallback):
        self.streamCallback = streamCallback #reference to the callback function for the stream setting
        self.servoCallback = servoCallback #reference to the callback function for either of the servo settings

        self.ref = None #reference to the database settings table
        self.cred = None #credentials to access the database
        self.initalizeFB() #initialize firebase stuff

    def initalizeFB(self): #function to initialize firebase stuff
        self.cred = credentials.Certificate(config.FB_CERT) #set the credentials
        firebase_admin.initialize_app(self.cred, config.FB_URL) #connect to the firebase

    def getSettings(self): #function to retrieve the settings from the database
        self.ref = db.reference(config.SETTINGS) #reference to the settings table in the database

        def listener(event): #function to trigger when updates happen
            key = event.path.lstrip('/') #get the name of the updated key
            value = event.data #get the value of the updated value
            print(f"Firebase event received: {key}: {value}")

            #trigger the callbacks depending on which key it was 
            if key == "Stream": 
                self.streamCallback(value)
            elif key == "ServoAngle" or key == "ServoDirection":
                self.servoCallback(key, value)

        self.ref.listen(listener) #listen for updates

