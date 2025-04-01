import asyncio
import queue
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

# Initialize Sense HAT
sense = SenseHat()
sense.clear()

# Audio Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
SILENCE_THRESHOLD = 500
MIN_AUDIO_LENGTH = 1.5

# Initialize Firebase
cred = credentials.Certificate("../../config/interprePi access key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com"
})

class AudioProcessor:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.buffer = deque(maxlen=int(RATE * 5 / CHUNK))
        self.recognizer = sr.Recognizer()
        self.is_hearing = False
        self.is_speaking = False
        self.current_gesture = ""
        self.loop = asyncio.new_event_loop()
        self.speaking_queue = queue.Queue()
        
    async def start_audio_stream(self):
        self.stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            stream_callback=self.audio_callback,
            start=False
        )
        
    def audio_callback(self, in_data, frame_count, time_info, status):
        if self.is_hearing:
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            if np.abs(audio_data).mean() > SILENCE_THRESHOLD:
                self.buffer.append(audio_data)
            elif len(self.buffer) > 0:
                asyncio.run_coroutine_threadsafe(self.process_audio_chunk(), self.loop)
        return (in_data, pyaudio.paContinue)
    
    async def process_audio_chunk(self):
        audio_segment = np.concatenate(self.buffer)
        self.buffer.clear()
        
        if len(audio_segment) < RATE * MIN_AUDIO_LENGTH:
            return
            
        audio_data = sr.AudioData(
            audio_segment.tobytes(), 
            sample_rate=RATE,
            sample_width=2
        )
        
        try:
            text = self.recognizer.recognize_google(audio_data)
            db.reference("Gestures/word").set(text)
            print(f"🔄 Transcribed: {text}")
            self.display_text(text, scroll_speed=0.05)
        except Exception as e:
            print(f"❌ Recognition error: {e}")
    
    def display_text(self, text, scroll_speed=0.1):
        """Display text on Sense HAT with optional scrolling"""
        sense.show_message(text, 
                         scroll_speed=scroll_speed,
                         text_colour=[255, 255, 255],
                         back_colour=[0, 0, 0])
        time.sleep(1)
        sense.clear()
    
    async def text_to_speech(self, text):
        print("I made it to TTS function")
        if not text:
            print("should be doing tts, but no text ig")
            print(text)
            return
            
        try:
            print(f"🔊 Speaking: {text}")
            # Display text first
            self.display_text(text)
            
            # Then speak it
            tts = gTTS(text=text, lang='en')
            tts.save('response.mp3')
            os.system('mpg321 -q response.mp3')
        except Exception as e:
            print(f"❌ TTS error: {e}")
    
    def start_firebase_listeners(self):
        def hearing_listener(event):
            self.is_hearing = event.data
            if self.is_hearing:
                print("✅ Listening mode ACTIVATED")
                self.stream.start_stream()
            else:
                print("⏸️ Listening mode PAUSED")
                self.stream.stop_stream()
                
        def speaking_listener(event):
            self.is_speaking = event.data
            if self.is_speaking:
                print("🎙️ Speaking mode ACTIVATED")
                # Check for current gesture immediately when speaking starts
                current = db.reference("Gestures/currentGesture").get()
                if current:
                    asyncio.run_coroutine_threadsafe(self.text_to_speech(current), self.loop)
            else:
                print("🔇 Speaking mode DEACTIVATED")
                
        def gesture_listener(event):
            new_gesture = event.data
            if new_gesture != self.current_gesture:
                self.current_gesture = new_gesture
                print(f"🔄 New gesture detected: {new_gesture}")
                print(self.is_speaking)
                if self.is_speaking:  # Only trigger TTS if in speaking mode
                    print("I should be speaking now")
                    asyncio.run_coroutine_threadsafe(self.text_to_speech(new_gesture), self.loop)
            
        db.reference("settings/3/isHearing").listen(hearing_listener)
        db.reference("settings/3/isSpeaking").listen(speaking_listener)
        db.reference("Gestures/currentGesture").listen(gesture_listener)
    
    async def run(self):
        await self.start_audio_stream()
        self.start_firebase_listeners()
        
        # Keep the application running
        while True:
            await asyncio.sleep(1)

async def main():
    processor = AudioProcessor()
    await processor.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sense.clear()
        print("🛑 Program stopped by user")
