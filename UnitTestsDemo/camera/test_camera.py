import unittest
import subprocess
import time

# Function to turn video stream on and off
def startStream(): 
    libcamera_vid_cmd = (
        "libcamera-vid --inline --width 800 --height 600 --framerate 30 --codec h264 --bitrate 500000 -t 0 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay ! udpsink host=192.168.1.102 port=5000"
    )
    # Start the GStreamer pipeline and capture errors
    process = subprocess.Popen(libcamera_vid_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for camera to start before returning
    time.sleep(5)

    # Kill camera after waiting
    process.terminate()
    process.wait()
    process = None

    # Removes preview window
    subprocess.run("pkill -f libcamera-vid", shell=True)

    return True

def verifyConnection():
    result = subprocess.run(['rpicam-hello'], capture_output=True, shell=True)
    out = result.stdout.strip().decode('utf-8')
    print(out)
    if ("ERROR" in out):
        return False
    else:
        return True

class TestCamera(unittest.TestCase):
    def test_connection(self):
        result = verifyConnection()
        self.assertTrue(result)
        

    def test_stream (self):
        result = startStream()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()