from camera.Camera import Camera
import asyncio

async def listener():
    print ("Listener: Starting...")
    Camera().listen()
    print (("Listener: Done"))

async def run_camera():
    print ("Camera: Starting...")
    Camera().runCamera()
    print ("Camera: Done")

async def main():
    await asyncio.gather(
        listener(),
        run_camera()
    )

asyncio.run(main())