import logging
import time
from enum import Enum
from langchain_core.tools import tool
from src.prompts.prompt_car_llm import prompt_user_car_agent, prompt_system_car_agent
from src.functions.functions_car import move_and_stop
from src.llm_services.OAI_image_to_text import image_to_text
from src.llm_services.OAI_text_to_speech import text_to_speech
from src.llm_services.OAI_text_to_text import text_to_text
from src.utils.audio import play_audio_with_pygame
from src.utils.camera import capture_image_from_ip_camera
from config.config import SPEECH_ENABLED
from src.utils.robot_context import RobotContext


class Movement(Enum):
    GO = "go"
    BACK = "back"
    LEFT = "left"
    RIGHT = "right"



@tool
def move_and_pic(movement: Movement, seconds: float, goal: str ) -> str:
    """
    This function moves you in specified directions based on input arguments,
    followed by capturing an image of the new location post-movement. It then analyzes the image to provide
    a description of the current scenario. The primary use of this function is to either approach an object for a closer
     examination, move away from or avoid obstacles, or to explore the surroundings.". The duration of movement,
    ranging from 0.1 to 2 seconds, should be adjusted based on the proximity to the nearest object,
    allowing you to make some calculations. For instance, a one-second movement advances forward by 50 cm,
    whereas turning left or right for the same duration results in a 180-degree turn.
    The outcome is a detailed description of the scene after repositioning, allowing for an assessment of whether
    the intended objective has been met.

    Parameters:
        movement: Specifies the direction of movement; options include 'go', 'back', 'left', 'right'.
        seconds: Duration of the movement, in seconds. It is crucial to utilize fractional values between 0.1 and 2 seconds.
                 Note that moving forward for 1 second covers a distance of 50 cm, significant relative to your size.
        goal: The objective intended to be achieved with the movement.
    """
    try:
        cycle_id = RobotContext.get_cycle_id()
        action_number = RobotContext.increment_action_counter()

        # Split the string at the dot
        movement = str(movement).split(".")
        movement = movement[1].lower()
        logging.info(f"[Cycle {cycle_id} - Action {action_number}] Initiating movement: {movement}, Duration: {seconds} seconds, Goal: {goal}")
        logging.info(f".............{movement}, {seconds}, {goal}")

        move_and_stop(str(movement).lower(), seconds )

        logging.info("sleeping after moving...")
        # Fixed 5-second wait to ensure the robot has completely stopped and stabilized before taking the next photo.
        # This is crucial to prevent blurriness and ensure accuracy in image capture.
        time.sleep(5)

        img_base64 = capture_image_from_ip_camera(cycle_id=cycle_id, action_number= action_number)
        prompt_user_car_agent_new = prompt_user_car_agent + f"""The goal we want to achieve is {goal}, so according to the 
        situation on the picture, we should provide a clear enough description to decide what action we need to take 
        next or if we have already reached the goal or if we should keep following it."""

        result = image_to_text(img_base64, prompt_system_car_agent, prompt_user_car_agent_new)
        logging.info(f"[Cycle {cycle_id} - Action {action_number}] - Result: {result}")

        if SPEECH_ENABLED:
            result_transformed = text_to_text(result + "." + goal)
            logging.info(f"[Cycle {cycle_id} - Action {action_number}] - Audio: {result}")
            content = result_transformed.choices[0].message.content
            audio = text_to_speech(content)
            play_audio_with_pygame(audio)

    except Exception as e:
        logging.error(f"An error occurred during move_and_pic operation: {e}")
        raise
    return result  # Access enum value
