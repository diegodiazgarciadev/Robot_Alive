import logging
import sounddevice as sd
from scipy.io.wavfile import write
import io
import pygame
import requests
from config.config import ESP32_IP_ROBOT, SPEECH_ENABLED

def record():
    # Configuration for recording
    fs = 44100  # Sampling rate
    duration = 10  # Duration in seconds
    file_path = '../../data/audio/output.wav'  # Audio file name

    logging.info("Recording...")

    try:
        # Record audio
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until the recording has finished

        # Save the audio file
        write(file_path, fs, myrecording)
    except Exception as e:
        logging.error(f"An error occurred during recording: {e}")
        return None

    logging.info("Recording completed successfully.")
    return file_path


def play_audio_with_pygame(audio_data):
    try:
        if not SPEECH_ENABLED:
            logging.info("Speech is disabled.")
            return None

        speak_url = f"http://{ESP32_IP_ROBOT}/speak"
        silence_url = f"http://{ESP32_IP_ROBOT}/silence"


        # Initialize pygame
        pygame.init()
        pygame.mixer.init()

        # Load audio data from a bytes object
        audio_file = io.BytesIO(audio_data)
        pygame.mixer.music.load(audio_file)

        requests.get(speak_url)
        logging.info("Robot starting to speak...")
        # Play the audio
        pygame.mixer.music.play()

        # Wait for the audio to finish playing (optional)
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        requests.get(silence_url)
        logging.info("Robot stopped speaking.")
        logging.info("Audio playback completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during audio playback: {e}")