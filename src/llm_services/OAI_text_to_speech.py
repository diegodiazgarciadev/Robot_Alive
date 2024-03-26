import logging
from openai import OpenAI
from config.config import OPENAI_API_KEY

def text_to_speech(text):
    """
      Converts text to speech using the OpenAI API.
      :param text: The text to be converted to speech.
      :return: The audio data of the spoken text.
      """
    try:
        logging.info("Converting text to speech...")
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )

        audio_data = response.content
        logging.info("Text to speech conversion successful.")
        return audio_data
    except Exception as e:
        logging.error(f"An error occurred during text to speech conversion: {e}")
        raise


