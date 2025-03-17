from flask import Flask, Response
from picamera2 import Picamera2
import io
from PIL import Image

from time import sleep


def initialize_camera():
    for _ in range(3):  # Retry 3 times
        try:
            picam2 = Picamera2()
            picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
            picam2.start()
            return picam2
        except Exception as e:
            print(f"Camera failed to initialize: {e}")
            sleep(2)  # Wait before retrying
    raise RuntimeError("Camera could not be initialized after multiple attempts.")

# Initialize the camera safely
picam2 = initialize_camera()





app = Flask(__name__)
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))  # Set resolution
picam2.start()

def generate_frames():
    while True:
        frame = picam2.capture_array()
        image = Image.fromarray(frame)
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        frame_bytes = buffer.getvalue()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return "Live Camera Feed - Use /video_feed to view"

@app.route('/?action=stream')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
