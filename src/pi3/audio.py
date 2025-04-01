import asyncio
import firebase_admin
from firebase_admin import credentials, db
import sounddevice as sd
import numpy as np
import speech_recognition as sr
from gtts import gTTS
import os
import pyaudio
from collections import deque
from sense_hat import SenseHat
import time
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize hardware
sense = SenseHat()
sense.clear()

# Audio Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
SILENCE_THRESHOLD = 500
MIN_AUDIO_LENGTH = 1.5

class AudioProcessor:
    def __init__(self):
        # Audio setup
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.buffer = deque(maxlen=int(RATE * 5 / CHUNK))
        self.recognizer = sr.Recognizer()
        
        # State management
        self.is_hearing = False
        self.is_speaking = False
        self.current_gesture = ""
        
        # Event loop setup
        self.loop = asyncio.new_event_loop()
        self.loop_thread = threading.Thread(target=self.start_loop, daemon=True)
        self.loop_thread.start()
        
        # Firebase setup
        cred = credentials.Certificate("../../config/interprePi access key.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com"
        })
        self.start_firebase_listeners()
        
        logger.info("System initialized")

    def start_loop(self):
        """Run the event loop in its own thread"""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def start_audio_stream(self):
        """Initialize audio stream"""
        self.stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            stream_callback=self.audio_callback,
            start=False
        )
        logger.info("Audio stream ready")

    def audio_callback(self, in_data, frame_count, time_info, status):
        """Handle incoming audio chunks"""
        if self.is_hearing:
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            if np.abs(audio_data).mean() > SILENCE_THRESHOLD:
                self.buffer.append(audio_data)
            elif len(self.buffer) > 0:
                asyncio.run_coroutine_threadsafe(
                    self.process_audio_chunk(), 
                    self.loop
                )
        return (in_data, pyaudio.paContinue)

    async def process_audio_chunk(self):
        """Process recorded audio"""
        audio_segment = np.concatenate(self.buffer)
        self.buffer.clear()
        
        if len(audio_segment) < RATE * MIN_AUDIO_LENGTH:
            return
            
        try:
            audio_data = sr.AudioData(
                audio_segment.tobytes(),
                sample_rate=RATE,
                sample_width=2
            )
            text = self.recognizer.recognize_google(audio_data)
            db.reference("Gestures/word").set(text)
            logger.info(f"Transcribed: {text}")
            await self.display_text(text)
        except Exception as e:
            logger.error(f"Recognition error: {e}")

    async def display_text(self, text, scroll_speed=0.1):
        """Display text on Sense HAT"""
        try:
            sense.show_message(
                text,
                scroll_speed=scroll_speed,
                text_colour=[255, 255, 255],
                back_colour=[0, 0, 0]
            )
            logger.debug(f"Displayed: {text}")
        except Exception as e:
            logger.error(f"Display error: {e}")

    async def text_to_speech(self, text):
        """Handle TTS and display"""
        if not text:
            return
            
        try:
            logger.info(f"Processing TTS for: {text}")
            
            # Display first
            await self.display_text(text)
            
            # Then speak
            tts = gTTS(text=text, lang='en')
            tts.save('response.mp3')
            os.system('mpg321 -q response.mp3')
            logger.info("TTS completed")
        except Exception as e:
            logger.error(f"TTS failed: {e}")

    def start_firebase_listeners(self):
        """Initialize Firebase listeners"""
        def hearing_listener(event):
            self.is_hearing = event.data
            status = "ACTIVE" if self.is_hearing else "PAUSED"
            logger.info(f"Listening mode: {status}")
            
            if self.is_hearing and not self.stream.is_active():
                self.stream.start_stream()
            elif not self.is_hearing and self.stream.is_active():
                self.stream.stop_stream()

        def speaking_listener(event):
            self.is_speaking = event.data
            logger.info(f"Speaking mode: {self.is_speaking}")
            
            if self.is_speaking:
                current = db.reference("Gestures/currentGesture").get()
                if current:
                    asyncio.run_coroutine_threadsafe(
                        self.text_to_speech(current),
                        self.loop
                    )

        def gesture_listener(event):
            if not self.is_speaking or not event.data:
                return
                
            if event.data != self.current_gesture:
                self.current_gesture = event.data
                logger.info(f"New gesture: {event.data}")
                asyncio.run_coroutine_threadsafe(
                    self.text_to_speech(event.data),
                    self.loop
                )

        # Start listeners
        db.reference("settings/3/isHearing").listen(hearing_listener)
        db.reference("settings/3/isSpeaking").listen(speaking_listener)
        db.reference("Gestures/currentGesture").listen(gesture_listener)
        logger.info("Firebase listeners active")

    async def run(self):
        """Main application loop"""
        await self.start_audio_stream()
        while True:
            await asyncio.sleep(1)

def main():
    processor = AudioProcessor()
    try:
        asyncio.run(processor.run())
    except KeyboardInterrupt:
        sense.clear()
        if processor.stream:
            processor.stream.stop_stream()
            processor.stream.close()
        processor.audio.terminate()
        logger.info("System shutdown complete")

if __name__ == "__main__":
    main()
