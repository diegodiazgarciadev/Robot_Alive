import logging
import requests
from src.functions.functions_car import distance
from config.config import OPENAI_API_KEY


def image_to_text (base64_image, prompt_system, prompt_user, ):
    """
    Calls OpenAI's API with an image and a user prompt to get a textual description of the image.
    :param base64_image: A base64 encoded image.
    :param prompt_system: The system prompt for OpenAI API.
    :param prompt_user: The user prompt for OpenAI API.
    :return: A textual message from the API's response.
    """
    logging.info("starting calling vision...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    try:
        dist = distance()
        prompt_with_distance = f"{prompt_user} keep in mind that you have a distance sensor measuring the closest object in front of you, and in this case, it's at a distance of {dist} cm"

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "system",
                    "content": prompt_system
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_with_distance
                        },

                        {
                            "type": "image_url",
                            "image_url": {
                                # Here we use the base64 image directly
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 150
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        # Convert the response into a Python dictionary
        response_json = response.json()

        # Accessing the specific message
        message = response_json['choices'][0]['message']['content']
        print(message)
        return message
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
    return None