import pyttsx3

def speak(text):
    engine = pyttsx3.init(driverName='espeak')  # Initialize the engine
    engine.say(text)
    engine.runAndWait()  # Wait for the speech to complete
    engine.stop()  # Ensure the engine is properly shut down

speak("Hello, this is a test.")
