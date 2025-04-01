import asyncio
from camera.Camera import Camera

async def main():
    camera = Camera()
    await camera.run()  # Camera handles async internally

asyncio.run(main()) 