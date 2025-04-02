import asyncio
import firebase_admin
from firebase_admin import credentials, db
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
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize hardware
sense = SenseHat()
sense.clear()

# Audio Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
SILENCE_THRESHOLD = 15  # Adjusted for better sensitivity
MIN_SPEECH_DURATION = 1.0  # Reduced minimum duration
MAX_SILENCE_GAP = 0.7  # Increased allowed gap

class AudioProcessor:
    def __init__(self):
        # Audio setup
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = SILENCE_THRESHOLD
        self.recognizer.dynamic_energy_threshold = True
        
        # Speech detection state
        self.speech_buffer = deque(maxlen=int(RATE * 10 / CHUNK))  # 10-second buffer
        self.speech_active = False
        self.last_loud_time = 0
        
        # State management
        self.is_hearing = False
        self.is_speaking = False
        self.current_gesture = ""
        
        # Event loop setup
        self.loop = asyncio.new_event_loop()
        self.loop_thread = threading.Thread(target=self.start_loop, daemon=True)
        self.loop_thread.start()
        
        # Initialize audio stream
        asyncio.run_coroutine_threadsafe(self.init_audio(), self.loop).result()
        
        # Firebase setup
        cred = credentials.Certificate("../../config/interprePi access key.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com"
        })
        self.start_firebase_listeners()
        
        logger.info("System initialized")

    def start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def init_audio(self):
        try:
            self.stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=self.audio_callback,
                start=False,
                input_device_index=None  # Auto-select default input
            )
            logger.info("Audio stream ready")
        except Exception as e:
            logger.error(f"Audio init failed: {e}")

    def audio_callback(self, in_data, frame_count, time_info, status):
        if not self.is_hearing:
            return (in_data, pyaudio.paContinue)
            
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        current_volume = np.abs(audio_data).mean()
        current_time = time.time()

        # Speech detection logic
        if current_volume > SILENCE_THRESHOLD:
            self.last_loud_time = current_time
            if not self.speech_active:
                self.speech_active = True
                logger.debug("Speech started")
            self.speech_buffer.append(audio_data)
        elif self.speech_active and (current_time - self.last_loud_time) < MAX_SILENCE_GAP:
            self.speech_buffer.append(audio_data)  # Keep recording through short pauses
        elif self.speech_active:
            # End of speech detected
            speech_duration = current_time - (self.last_loud_time - MAX_SILENCE_GAP)
            if speech_duration >= MIN_SPEECH_DURATION:
                asyncio.run_coroutine_threadsafe(
                    self.process_speech(), 
                    self.loop
                )
            self.speech_active = False
            self.speech_buffer.clear()
            logger.debug("Speech ended")
                
        return (in_data, pyaudio.paContinue)

    async def process_speech(self):
        if not self.speech_buffer:
            return
            
        audio_segment = np.concatenate(list(self.speech_buffer))
        try:
            # Convert to speech_recognition AudioData
            audio_data = sr.AudioData(
                audio_segment.tobytes(),
                sample_rate=RATE,
                sample_width=2  # 16-bit = 2 bytes
            )
            
            # Try Google STT with timeout
            text = self.recognizer.recognize_google(
                audio_data, 
                language="en-US",
                show_all=False
            )
            
            logger.info(f"Transcribed: {text}")
            db.reference("Gestures/word").set(text)
            await self.display_text(text)
            
        except sr.UnknownValueError:
            logger.debug("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    async def display_text(self, text):
        try:
            sense.show_message(text, 
                             scroll_speed=0.1,
                             text_colour=[255, 255, 255],
                             back_colour=[0, 0, 0])
        except Exception as e:
            logger.error(f"Display error: {e}")

    async def text_to_speech(self, text):
        if not text:
            return
            
        try:
            logger.info(f"Speaking: {text}")
            await self.display_text(text)
            
            tts = gTTS(text=text, lang='en')
            tts.save('response.mp3')
            os.system('mpg321 -q response.mp3')
        except Exception as e:
            logger.error(f"TTS error: {e}")

    def start_firebase_listeners(self):
        def hearing_listener(event):
            self.is_hearing = event.data
            if not self.stream:
                return
                
            if self.is_hearing and not self.stream.is_active():
                self.stream.start_stream()
                logger.info("Listening mode: ACTIVE")
            elif not self.is_hearing and self.stream.is_active():
                self.stream.stop_stream()
                logger.info("Listening mode: PAUSED")

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

        db.reference("settings/3/isHearing").listen(hearing_listener)
        db.reference("settings/3/isSpeaking").listen(speaking_listener)
        db.reference("Gestures/currentGesture").listen(gesture_listener)
        logger.info("Firebase listeners active")

    async def run(self):
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
        logger.info("System shutdown")

if __name__ == "__main__":
    main()
