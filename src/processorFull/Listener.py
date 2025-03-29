import firebase_admin
from firebase_admin import credentials, db

from processorFull import config

class Listener:
    def __init__(self, streamCallback):
        self.streamCallback = streamCallback

        self.settingsRef = None
        self.gesturesRef = None
        self.cred = None
        self.initalizeFB()

    def initalizeFB(self):
        self.cred = credentials.Certificate(config.FB_CERT)
        firebase_admin.initialize_app(self.cred, config.FB_URL)

    def getSettings(self):
        self.settingsRef = db.reference(config.SETTINGS)

        def streamListener(event):
            key = event.path.lstrip('/')
            value = event.data
            print(f"Firebase event received: {key}: {value}")

            if key == "Stream":
                self.streamCallback(value)
            elif isinstance(value, dict) and "Stream" in value:
                self.streamCallback(value["Stream"])

        self.settingsRef.listen(streamListener)

    def updateFirebase(self, symbol):
        self.gesturesRef = db.reference(config.GESTURES)
        try: 
            current = self.gesturesRef.child('currentGesture').get()
            updates = {
                'prevGesture': current,
                'currentGesture': symbol
            }
            self.gesturesRef.update(updates)
        except Exception as e:
            print(f"❌ Firebase update failed: {str(e)}")


