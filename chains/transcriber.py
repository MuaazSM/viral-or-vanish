from transformers import pipeline
import torch

# Load Whisper pipeline once
asr_pipeline = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large-v3",
    device=0 if torch.cuda.is_available() else -1
)

def transcribe_audio_to_text(audio_file_path: str) -> str:
    """Transcribe audio file to text using Whisper."""
    try:
        result = asr_pipeline(audio_file_path)
        return result["text"].strip()
    except Exception as e:
        print(f"Error transcribing audio with Whisper: {e}")
        return ""

