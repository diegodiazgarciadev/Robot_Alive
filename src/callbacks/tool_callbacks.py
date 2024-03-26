import logging
from typing import Any
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from src.llm_services.OAI_text_to_speech import text_to_speech
from src.llm_services.OAI_text_to_text import text_to_text
from src.utils.audio import play_audio_with_pygame
from config.config import SPEECH_ENABLED



class AgentCallbackHandler(BaseCallbackHandler):


    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Handler for the end of the LLM's processing."""
        logging.info("------------------------------")
        logging.info(f"----Response action_input:---\n{response.generations[0][0].text}")
        logging.info("------------------------------")
        import json

        # Extracting the text from the generation, which is a JSON object
        generation_text = response.generations[0][0].text
        # Finding the start and end of the JSON object
        json_start_index = generation_text.find('{')
        json_end_index = generation_text.rfind('}') + 1
        # Extracting the JSON text from the start of the JSON object to the end of the JSON object
        json_text = generation_text[
                    json_start_index:json_end_index] if json_start_index != -1 and json_end_index != -1 else ""

        # Attempting to directly parse the JSON
        try:
            action_data = json.loads(json_text)
            # Checking if the 'action' is "Final Answer"
            if action_data.get('action') == 'Final Answer':
                # If so, print only the 'action_input'
                logging.info("***Action Input:***")
                logging.info(action_data['action_input'])
                if SPEECH_ENABLED:
                    self.speak_action_input(action_data['action_input'])
            else:
                logging.info("Action was not 'Final Answer'.")
        except json.JSONDecodeError:
            # In case of a JSON decoding error, print an error message
            logging.error(f"Error decoding JSON in the response: {e}")

    def speak_action_input(self, action_input: str):
        """Converts action input to speech."""
        content_system = (
            "Alright, we've either reached the end, achieved our goal, or... ah, "
            "possibly failed. Just give a really brief explanation on why no actions were taken and we've "
            "concluded. The reason for this wrap-up will be found in the 'prompt_user."
        )
        result_transformed = text_to_text(action_input, content_system)
        content = result_transformed.choices[0].message.content
        audio = text_to_speech(content)
        play_audio_with_pygame(audio)