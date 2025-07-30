import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from chains.prompt_templates import WRITER_TEMPLATE, EVALUATOR_TEMPLATE
from chains.transcriber import transcribe_audio_to_text  # Now uses Whisper
import json

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.8,
    max_tokens=512,
)

# Speech transcription function
def transcribe_audio_to_text(audio_file_path: str) -> str:
    """Transcribe audio file to text using Google Cloud Speech-to-Text.
    """
    try:
        transcript = transcribe_audio_to_text(audio_file_path)
        return transcript
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return ""

# Writer Chain
def get_writer_response(prompt_text: str, tone: str, audio_file: str = None) -> dict:
    """Get AI writer response with optional audio input.
    """
    # If audio file is provided, transcribe it and use as additional context
    audio_context = ""
    if audio_file:
        audio_context = transcribe_audio_to_text(audio_file)
        if audio_context:
            # Add audio context to the prompt
            prompt_text = f"{prompt_text}\n\nAudio context: {audio_context}"
    
    prompt = PromptTemplate(
        input_variables=["prompt", "tone"],
        template=WRITER_TEMPLATE
    )
    chain = prompt | llm
    response = chain.invoke({"prompt": prompt_text, "tone": tone})
    
    return {
        "ai_pitch": response.content.strip(),
        "tone": tone,
        "audio_transcript": audio_context if audio_file else None
    }

# Evaluator Chain
def get_evaluation_result(prompt_text: str, human: str, ai: str, tone: str, human_audio: str = None) -> dict:
    """Evaluate human vs AI responses with optional audio input.
    """
    # If human provided audio, transcribe it and use instead of/alongside text
    if human_audio:
        audio_transcript = transcribe_audio_to_text(human_audio)
        if audio_transcript:
            human = audio_transcript  # Use transcribed audio as human response
    
    prompt = PromptTemplate(
        input_variables=["prompt", "human", "ai", "tone"],
        template=EVALUATOR_TEMPLATE
    )
    chain = prompt | llm
    response = chain.invoke({
        "prompt": prompt_text,
        "human": human,
        "ai": ai,
        "tone": tone
    })

    # trying to parse JSON if gemini returns it, else fallback to text
    try:
        eval_json = json.loads(response.content)
    except:
        eval_json = {
            "verdict_text": response.content,
            "score_human": None,
            "score_ai": None,
            "winner": None
        }

    return eval_json

# Legacy functions to maintain compatibility
def get_writer_chain():
    """Legacy function for backward compatibility."""
    class WriterChain:
        def invoke(self, inputs):
            result = get_writer_response(inputs["prompt"], inputs["tone"])
            class Response:
                def __init__(self, content):
                    self.content = content
            return Response(result["ai_pitch"])
    return WriterChain()

def get_evaluator_chain():
    """Legacy function for backward compatibility."""
    class EvaluatorChain:
        def invoke(self, inputs):
            result = get_evaluation_result(
                inputs["prompt"], 
                inputs["human"], 
                inputs["ai"], 
                inputs["tone"]
            )
            class Response:
                def __init__(self, content):
                    self.content = content
            return Response(result["verdict_text"])
    return EvaluatorChain()