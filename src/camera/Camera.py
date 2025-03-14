import os
import subprocess
import time

from camera import config
from camera.Listener import Listener

class Camera:
    def __init__(self):
        self.IPScriptPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "addip.sh")
        subprocess.run(['bash', self.IPScriptPath]) 
        self.listener = Listener(self.stream)
        self.process = None
        

    def runCamera(self):
        self.process = subprocess.Popen(config.VID_CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        while True:
            time.sleep(1)

    def stopCamera(self):
        if self.process:
            self.process.terminate()
            self.process = None
            print("Camera stopped")

    def stream(self, enabled):
        if enabled:
            print("Camera enabled")
            self.runCamera()
        else:
            print("Camera disabled")
            self.stopCamera()
        
    def listen(self):
        while True:
            self.listener.getSettings()
        