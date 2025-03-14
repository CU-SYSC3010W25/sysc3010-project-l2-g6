import os
import subprocess
import time

from camera import config

class Camera:
    def __init__(self):
        self.IPScriptPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "addip.sh")
        subprocess.run(['bash', self.IPScriptPath]) 

    def runCamera(self):
        process = subprocess.Popen(config.VID_CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        while True:
            time.sleep(1)
