import threading
import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import logging

# HTML template for web interface
PAGE = """\
<html>
<head>
<title>Camera Stream</title>
</head>
<body>
<center><h1>Live Camera Stream</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
</body>
</html>
"""

class StreamingOutput:
    def __init__(self):
        self.frame = None
        self.condition = threading.Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class StreamingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning('Client disconnected: %s', str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

def capture_frames():
    # Initialize camera capture
    cap = cv2.VideoCapture(0)  # 0 for default camera
    
    # Set camera resolution (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Convert frame to JPEG
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue
                
            # Write JPEG to output
            output.write(jpeg.tobytes())
    finally:
        cap.release()

# Global streaming output
output = StreamingOutput()

if __name__ == '__main__':
    try:
        # Start frame capture thread
        capture_thread = threading.Thread(target=capture_frames, daemon=True)
        capture_thread.start()
        
        # Start streaming server
        address = ('172.17.174.224', 8000)
        server = StreamingServer(address, StreamingHandler)
        print("Server started at http://localhost:8000")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.shutdown()