import os
import subprocess
import asyncio
import time
from camera import config
from camera.Listener import Listener

class Camera:
    def __init__(self):
        self.IPScriptPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "addip.sh")
        subprocess.run(['bash', self.IPScriptPath])  # Set IP address on startup
        
        self.listener = Listener(self.stream)
        self.process = None
        self.running = False

    async def run(self):
        """Starts both the camera and Firebase listener asynchronously."""
        await asyncio.gather(
            self.listen_for_changes(),  # Run Firebase listener
            self.start_stream()  # Run camera stream
        )

    async def start_stream(self):
        """Manages video streaming, allowing it to be dynamically turned on/off."""
        while True:
            if self.running and self.process is None:
                print("✅ Starting Camera Stream...")
                self.process = subprocess.Popen(config.VID_CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            elif not self.running and self.process:
                print("⛔ Stopping Camera Stream...")
                self.process.terminate()
                self.process = None

            await asyncio.sleep(1)  # Sleep briefly before rechecking

    def stream(self, enabled):
        """Callback function to enable/disable the camera."""
        self.running = enabled
        print(f"🔥 Camera {'enabled' if enabled else 'disabled'}")

    async def listen_for_changes(self):
        """Runs the Firebase listener asynchronously."""
        await asyncio.to_thread(self.listener.getSettings)

