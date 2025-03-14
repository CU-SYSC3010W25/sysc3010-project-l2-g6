import firebase_admin
from firebase_admin import credentials, db

from processor import config

class Listener:
    def __init__(self, callback):
        self.callback = callback

        self.ref = None
        self.cred = None
        self.initalize_FB()

    def initalize_FB(self):
        self.cred = credentials.Certificate(config.FB_CERT)
        firebase_admin.initialize_app(self.cred, config.FB_URL)

    def getSettings(self):
        self.ref = db.reference(config.SETTINGS)

        def streamListener(event):
            print(f"Firebase event received: {event.path.lstrip('/')}: {event.data}")
            self.callback(event.data)

        self.ref.listen(streamListener)

