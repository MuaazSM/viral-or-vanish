# whisper or google STT integration
import openai
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(audio_bytes) -> str:
    # save to temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_path = tmp_file.name

    # transcribe using whisper
    with open(tmp_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    return transcript["text"]