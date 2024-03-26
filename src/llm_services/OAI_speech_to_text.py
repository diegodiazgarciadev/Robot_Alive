import logging
from openai import OpenAI
from config.config import OPENAI_API_KEY

def audiofile_to_text (audiofile_path):
    """
    Transcribes an audio file to text using the OpenAI API.
    :param audiofile_path: The file path to the audio file.
    :return: The transcribed text.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    logging.info("Transcribing...")
    try:
        # Open the audio file and send it for transcription
        with open(audiofile_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
              model="whisper-1",
              file=audio_file
            )
            transcribed_text = transcription.get("text", "")
            logging.info(f"Transcription successful: {transcribed_text}")
            return transcribed_text
    except Exception as e:
        logging.error(f"An error occurred during transcription: {e}")
        raise

