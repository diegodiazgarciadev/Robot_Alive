import logging
from PIL import Image
import io
import base64
import requests
import cv2
from config.config import CAMERA_IP_URL,ESP32_CAM_URL
import datetime
import os


def image_to_base64(pil_image):
    """
    Converts a PIL Image to a base64 string without saving it to disk.
    """
    buffered = io.BytesIO()
    pil_image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def capture_and_process_frame(esp32_cam_ip=ESP32_CAM_URL, skip_frames=2):
    """
    Captures and processes a frame from an ESP32 cam stream.
    """
    try:
        with requests.get(esp32_cam_ip, stream=True) as response:
            response.raise_for_status()
            bytes_data = b''
            frames_skipped = 0
            for chunk in response.iter_content(chunk_size=1024):
                bytes_data += chunk
                while True:
                    a = bytes_data.find(b'\xff\xd8')  # Start of a JPEG image
                    b = bytes_data.find(b'\xff\xd9', a + 2)  # End of a JPEG image
                    if a != -1 and b != -1:
                        if frames_skipped >= skip_frames:
                            jpg = bytes_data[a:b+2]  # Extract JPEG
                            image = Image.open(io.BytesIO(jpg))
                            rotated_image = image.rotate(-90, expand=True)
                            base64_image = image_to_base64(rotated_image)
                            return base64_image
                        else:
                            frames_skipped += 1
                            bytes_data = bytes_data[b+2:]
                    else:
                        break
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to connect to the camera: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    return None




def ensure_directory_exists(directory_path):
    """Asegura que el directorio especificado existe, creándolo si es necesario."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def capture_image_from_ip_camera(camera_url=CAMERA_IP_URL, cycle_id=None, action_number=None):
    """
    Captures an image from an IP camera, saves it to disk including cycle_id and action_number in the filename,
    and returns the base64 encoded image.
    """
    try:
        cap = cv2.VideoCapture(camera_url)
        if not cap.isOpened():
            logging.error("Error: Could not open video stream.")
            return None

        ret, frame = cap.read()
        if ret:
            images_directory = "data/images/captured_images"
            ensure_directory_exists(images_directory)

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_suffix = f"{cycle_id}_{action_number}" if cycle_id and action_number else "uncategorized"
            image_filename = f"{images_directory}/captured_image_{file_suffix}_{timestamp}.jpg"


            pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            pil_image.save(image_filename)  # Save image to disk
            logging.info(f"Image captured and saved: {image_filename}")
            base64_image = image_to_base64(pil_image)
            return base64_image
        else:
            logging.error("Error: Could not read frame from video.")
    except Exception as e:
        logging.error(f"An error occurred during capture: {e}")
    return None

