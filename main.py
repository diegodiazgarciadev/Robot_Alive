import logging
from src.llm_services.OAI_text_to_speech import text_to_speech
from src.llm_services.OAI_text_to_text import text_to_text
from src.utils.audio import play_audio_with_pygame
from src.utils.camera import capture_image_from_ip_camera
from src.llm_services.OAI_image_to_text import image_to_text
from src.prompts.prompt_car_llm import prompt_user, prompt_system
from src.agents.goal import goal_agent,move_and_pic
from config.config import SPEECH_ENABLED,CAPTURE_INTERVAL_SECONDS,LOG_LEVEL
import time
import warnings


numeric_level = getattr(logging, LOG_LEVEL.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError(f'Invalid log level: {LOG_LEVEL}')
logging.basicConfig(level=numeric_level)
warnings.filterwarnings("ignore", category=DeprecationWarning,)

tools = [move_and_pic]

def start():
    while True:
        logging.info("Capturing image...")
        base64_image  = capture_image_from_ip_camera()
        if base64_image:
            logging.info("Image captured successfully. Entering main loop...")
            time.sleep(1)
            # This was a test for changing the prompts at runtime.
            # content_user = f"""If you don't like these prompts, want to modify them to improve them,
            #                    or because you're bored with this behavior, change them. The response should be
            #                    similar to the current prompts, you should return two:
            #                    1.- prompt_system: here you define the system prompt considering that the tools
            #                    you have at your disposal are {tools}
            #                    2.- prompt_user: here you define the user prompt considering that the tools
            #                    you have at your disposal are {tools}
            #                    """
            # content_system= prompt_system + "\n" + prompt_user
            # response= text_to_text(content_user, content_system)
            # print(response)
            try:
                # calling vision
                message_with_goal = image_to_text(base64_image, prompt_system, prompt_user)

                if SPEECH_ENABLED:
                    logging.info("Generating speech from text...")
                    result_transformed = text_to_text(message_with_goal)
                    content = result_transformed.choices[0].message.content
                    audio = text_to_speech(content)
                    play_audio_with_pygame(audio)
                    logging.info("Speech played successfully.")
                else:
                    logging.info("Speech is disabled. Skipping speech synthesis.")

                goal_agent(message_with_goal)

            except Exception as e:
                logging.error(f"An error occurred during the main loop: {e}")
        else:
            logging.warning("No image captured. Skipping this cycle.")
        # Wait CAPTURE_INTERVAL_SECONDS seconds before the next capture
        logging.info(f"Sleeping {CAPTURE_INTERVAL_SECONDS} seconds before the next capture...")
        time.sleep(CAPTURE_INTERVAL_SECONDS)

if __name__ == '__main__':
    logging.info('Robot LLM proyect')
    start()

