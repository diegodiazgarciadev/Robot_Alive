import logging
from openai import OpenAI
from config.config import OPENAI_API_KEY

content_system_default = ("Please, Use the most natural language possible, including interjections like hmm, ehh. "
                          " It's like your thoughts, but you're going to say them out loud. "
                          " Summarize it in about 50 tokens and write energetically, as if you're feeling very alive."
                          " Keep in mind it will be listened to by people, so it should be as natural as possible."
                          " You don't need to provide data about your speed, nor the proximity of objects in cm."
                          " Speak in the first person to make it more real and engaging. Say it all in 50 tokens")


def text_to_text(content_user, content_system=content_system_default):
    try:
        logging.info("Requesting text-to-text transformation...")
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": content_system},
                {"role": "user", "content": content_user},
            ]
        )
        logging.info("Text-to-text request successful.")
        return response
    except Exception as e:
        logging.error(f"An error occurred during text-to-text transformation: {e}")
        raise



