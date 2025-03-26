import sounddevice as sd
import soundfile as sf
import numpy as np

# Audio settings
RATE = 44100              # Sampling rate (44.1 kHz)
CHANNELS = 1              # Mono audio (or 2 for stereo)
RECORD_SECONDS = 5        # Duration of recording in seconds
WAVE_OUTPUT_FILENAME = "output.wav"  # File to save the recorded audio

# Function to record audio from the default microphone
def record_audio():
    print("🎤 Recording audio...")

    # Record audio
    audio_data = sd.rec(int(RECORD_SECONDS * RATE), samplerate=RATE, channels=CHANNELS, dtype='float32')
    sd.wait()  # Wait until recording is finished

    print("✅ Recording complete.")

    # Save the recorded audio to a WAV file
    sf.write(WAVE_OUTPUT_FILENAME, audio_data, RATE)
    print(f"💾 Saved recording to {WAVE_OUTPUT_FILENAME}")

# Function to play audio through the default speakers
def play_audio():
    print("🔊 Playing audio...")

    # Load the WAV file
    audio_data, sample_rate = sf.read(WAVE_OUTPUT_FILENAME, dtype='float32')

    # Play audio
    sd.play(audio_data, sample_rate)
    sd.wait()  # Wait until playback is finished

    print("✅ Playback complete.")

# Main function
def main():
    try:
        # Record audio from the microphone
        record_audio()

        # Play the recorded audio through the speakers
        play_audio()
    except Exception as e:
        print(f"❌ An error occurred: {e}")

# Run the script
if __name__ == "__main__":
    main()
