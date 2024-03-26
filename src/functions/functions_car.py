import logging
import requests
from config.config import ESP32_IP_ROBOT


def move_and_stop(direction, duration):
    """
    Moves the car in a specified direction, waits for a while, and then stops it.
    :param direction: Direction of movement ('go', 'back', 'left', 'right').
    :param duration: Duration of the movement in seconds.
    """
    logging.info("Calling car to move....")

    move_url = f"http://{ESP32_IP_ROBOT}/{direction}"
    # Parameters for the GET request
    params = {'time': duration}
    try:
        response = requests.get(move_url, params=params)
        if response.status_code == 200:
            logging.info(f"Car moved {direction} and stopped.")
        else:
            logging.error(f"Error moving car in {direction} direction: HTTP {response.status_code}")
    except Exception as e:
        logging.exception(f"Exception occurred while moving the car: {e}")

def distance():

    url = f'http://{ESP32_IP_ROBOT}/distance'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            distance = response.text.strip()
            logging.info(f"Distance: {distance} cm")
            return distance
        else:
            logging.error(f"Error fetching distance: HTTP {response.status_code}")
    except Exception as e:
        logging.exception(f"Exception occurred while fetching distance: {e}")
