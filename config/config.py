# src/config.py
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ESP32_IP_ROBOT = "192.168.1.148"
CAMERA_IP_URL = "http://192.168.1.149:8080/video"
ESP32_CAM_URL = "http://192.168.1.142:81/stream"
SPEECH_ENABLED = True
CAPTURE_INTERVAL_SECONDS = 10
LOG_LEVEL = "INFO"

