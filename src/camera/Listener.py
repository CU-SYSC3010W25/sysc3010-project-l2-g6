import firebase_admin
from firebase_admin import credentials, db

from camera import config

class Listener:
    def __init__(self, streamCallback, servoCallback):
        self.streamCallback = streamCallback
        self.servoCallback = servoCallback

        self.ref = None
        self.cred = None
        self.initalizeFB()

    def initalizeFB(self):
        self.cred = credentials.Certificate(config.FB_CERT)
        firebase_admin.initialize_app(self.cred, config.FB_URL)

    def getSettings(self):
        self.ref = db.reference(config.SETTINGS)

        def listener(event):
            key = event.path.lstrip('/')
            value = event.data
            print(f"Firebase event received: {key}: {value}")

            if key == "Stream":
                self.streamCallback(value)
            elif key == "ServoAngle":
                self.servoCallback(key, value)

        self.ref.listen(listener)

