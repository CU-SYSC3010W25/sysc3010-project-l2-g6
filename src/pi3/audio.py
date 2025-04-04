import asyncio
import firebase_admin
from firebase_admin import credentials, db
import sounddevice as sd
import numpy as np
import speech_recognition as sr
from gtts import gTTS
import os
import time
import logging
from sense_hat import SenseHat
import queue

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize hardware
sense = SenseHat()
sense.clear()

# Audio Configuration
RATE = 16000
CHUNK_SIZE = 1024
MAX_RECORD_SECONDS = 15

class AudioProcessor:
    def __init__(self):
        # Recording state
        self.is_recording = False
        self.audio_buffer = []
        self.recording_start_time = 0
        
        # System state
        self.is_hearing = False
        self.is_speaking = False
        self.current_gesture = ""
        
        # Thread-safe communication
        self.command_queue = queue.Queue()
        
        # Initialize Firebase
        cred = credentials.Certificate("../../config/interprePi access key.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com"
        })
        self._setup_firebase()
        
        # Setup joystick handler
        sense.stick.direction_any = self._joystick_handler
        
        logger.info("System ready. Joystick controls recording when isHearing=True")

    def _setup_firebase(self):
        """Configure Firebase listeners"""
        def hearing_listener(event):
            self.is_hearing = event.data
            logger.info(f"isHearing set to: {self.is_hearing}")
            if not self.is_hearing and self.is_recording:
                self.command_queue.put(("stop_recording", None))

        def speaking_listener(event):
            self.is_speaking = event.data
            logger.info(f"isSpeaking set to: {self.is_speaking}")

        def gesture_listener(event):
            if self.is_speaking and event.data:
                if event.data != "nothing" or event.data != "del":
                    self.current_gesture = event.data
                    self.command_queue.put(("text_to_speech", event.data))

        db.reference("settings/3/isHearing").listen(hearing_listener)
        db.reference("settings/3/isSpeaking").listen(speaking_listener)
        db.reference("Gestures/currentGesture").listen(gesture_listener)

    def _joystick_handler(self, event):
        """Handle joystick button presses"""
        if event.action == 'pressed' and self.is_hearing:
            if not self.is_recording:
                self.command_queue.put(("start_recording", None))
            else:
                self.command_queue.put(("stop_recording", None))

    async def _start_recording(self):
        """Begin audio recording"""
        if self.is_recording:
            return
            
        self.is_recording = True
        self.audio_buffer = []
        self.recording_start_time = time.time()
        
        # Start audio stream
        self.stream = sd.InputStream(
            samplerate=RATE,
            blocksize=CHUNK_SIZE,
            channels=1,
            dtype='int16',
            callback=self._audio_callback
        )
        self.stream.start()
        
        sense.show_letter("R", text_colour=[255, 0, 0])  # Red R for recording
        logger.info("Recording started")

    async def _stop_recording(self):
        """Stop recording and process audio"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        self.stream.stop()
        self.stream.close()
        
        sense.show_letter("P", text_colour=[0, 255, 0])  # Green P for processing
        logger.info("Recording stopped")
        
        # Process the recorded audio
        await self._process_recording()

    def _audio_callback(self, indata, frames, time_info, status):
        """Collect audio chunks while recording"""
        if self.is_recording:
            self.audio_buffer.append(indata.copy())
            
            # Auto-stop if exceeding max duration
            if time.time() - self.recording_start_time > MAX_RECORD_SECONDS:
                self.command_queue.put(("stop_recording", None))

    async def _process_recording(self):
        """Process the recorded audio"""
        try:
            # Combine audio chunks
            audio_data = np.concatenate(self.audio_buffer)
            
            # Convert to speech_recognition format
            audio = sr.AudioData(
                audio_data.tobytes(),
                sample_rate=RATE,
                sample_width=2
            )
            
            # Transcribe
            text = sr.Recognizer().recognize_google(audio)
            logger.info(f"Transcribed: {text}")
            
            # Push to Firebase
            db.reference("Gestures/word").set(text)
            
            # Display result
            sense.show_message(text, scroll_speed=0.1)
            
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            sense.show_message("?", text_colour=[255, 255, 0])
        except Exception as e:
            logger.error(f"Processing error: {e}")
            sense.show_message("!", text_colour=[255, 0, 0])
        finally:
            sense.clear()

    async def text_to_speech(self, text):
        """Convert text to speech"""
        if not text:
            return
            
        try:
            if text == "nothing":
                return
            if text == "del":
                return
            if text == "space":
                return
            if text == "clear":
                return
            
            # Speak first
            tts = gTTS(text=text, lang='en')
            tts.save('response.mp3')
            os.system('mpg321 -q response.mp3')
            # Then display text
            sense.show_message(text, scroll_speed=0.1)
        except Exception as e:
            logger.error(f"TTS error: {e}")

    async def run(self):
        """Main application loop"""
        while True:
            # Process commands from queue
            try:
                cmd, arg = self.command_queue.get_nowait()
                if cmd == "start_recording":
                    await self._start_recording()
                elif cmd == "stop_recording":
                    await self._stop_recording()
                elif cmd == "text_to_speech":
                    await self.text_to_speech(arg)
            except queue.Empty:
                pass
            
            await asyncio.sleep(0.1)

def main():
    processor = AudioProcessor()
    try:
        asyncio.run(processor.run())
    except KeyboardInterrupt:
        sense.clear()
        if hasattr(processor, 'stream') and processor.stream:
            processor.stream.stop()
            processor.stream.close()
        logger.info("System shutdown")

if __name__ == "__main__":
    main()
