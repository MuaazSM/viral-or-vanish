import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from chains.prompt_templates import WRITER_TEMPLATE, EVALUATOR_TEMPLATE
from chains.transcriber import transcribe_audio_to_text
import json

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.8,
    max_tokens=512,
)

# writer chain
def get_writer_response(prompt_text: str) -> dict:
    prompt = PromptTemplate(
        input_variables=["prompt"],
        template=WRITER_TEMPLATE
    )
    chain = prompt | llm
    response = chain.invoke({"prompt": prompt_text})

    return {
        "ai_pitch": response.content.strip()
    }


# Evaluator Chain
def get_evaluation_result(prompt_text: str, human: str, ai: str, tone: str, human_audio: str = None) -> dict:
    """
    Evaluate human vs AI responses with audio input
    """
    # if human provided audio, transcribe it and use instead of/alongside text
    if human_audio:
        audio_transcript = transcribe_audio_to_text(human_audio)
        if audio_transcript:
            human = audio_transcript  # use transcribed audio as human response
    
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