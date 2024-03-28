import logging
import json
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
        try:
            # Attempt to log the response from LLM.
            logging.info(f"----Response action_input:---\n{response.generations[0][0].text}")
            logging.info("------------------------------")

            # Process the LLM result.
            self.process_llm_result(response.generations[0][0].text)
        except IndexError as e:
            # Log if there's an issue with accessing the response.
            logging.error(f"Error accessing LLM response: {e}")
        except Exception as e:
            # Log any other errors that might occur.
            logging.error(f"An unexpected error occurred: {e}")

    def process_llm_result(self, generation_text: str):
        """Processes the LLM result and potentially speaks the action input."""
        try:
            logging.info(f"***generation_text: {generation_text}")
            action_data = self.extract_action_data(generation_text)
            logging.info(f"***action_data: {action_data}")
            if action_data and action_data.get('action') == 'Final Answer':
                logging.info("***Action Input:***")
                logging.info(action_data['action_input'])
                if SPEECH_ENABLED:
                    self.speak_action_input(action_data['action_input'])
            else:
                logging.info("Action was not 'Final Answer' or no actionable data found.")
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON in the response: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred while processing LLM result: {e}")

    @staticmethod
    def extract_action_data(generation_text: str) -> dict:
        """Attempts to extract action data from the generation text."""
        json_start_index = generation_text.find('{')
        json_end_index = generation_text.rfind('}') + 1
        json_text = generation_text[json_start_index:json_end_index] if json_start_index != -1 and json_end_index != -1 else ""
        return json.loads(json_text) if json_text else {}

    def speak_action_input(self, action_input: str):
        """Converts action input to speech."""
        content_system = (
            "Alright, we've either reached the end, achieved our goal, or "
            "possibly failed. Just give a really brief explanation on why no actions were taken and we've "
            "concluded. The reason for this wrap-up will be found in the 'prompt_user', and you finish "
            "saying something, let's find another thing to do."
        )
        try:
            result_transformed = text_to_text(action_input, content_system)
            content = result_transformed.choices[0].message.content
            audio = text_to_speech(content)
            play_audio_with_pygame(audio)
        except Exception as e:
            logging.error(f"Error while converting action input to speech: {e}")
