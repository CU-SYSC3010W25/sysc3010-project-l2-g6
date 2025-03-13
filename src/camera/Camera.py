import subprocess
import time

from camera import config

class Camera:
    def __init__(self):
        pass

    def runCamera():
        process = subprocess.Popen(config.VID_CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        while True:
            time.sleep(1)
