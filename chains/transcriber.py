from transformers import pipeline
import torch

asr_pipeline = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small", 
    device=0 if torch.cuda.is_available() else -1,
    generate_kwargs={"task": "transcribe", "language": "en"}
)


def transcribe_audio_to_text(audio_file_path: str) -> str:
    """Transcribe audio using Whisper"""
    try:
        result = asr_pipeline(audio_file_path)
        return result["text"].strip()
    except Exception as e:
        print(f"Error transcribing audio with Whisper: {e}")
        return ""
