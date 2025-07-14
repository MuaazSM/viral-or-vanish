import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from chains.prompt_templates import WRITER_TEMPLATE, EVALUATOR_TEMPLATE
import json

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.8,
    max_tokens=512,
)

# Writer Chain
def get_writer_response(prompt_text: str, tone: str) -> dict:
    prompt = PromptTemplate(
        input_variables=["prompt", "tone"],
        template=WRITER_TEMPLATE
    )
    chain = prompt | llm
    response = chain.invoke({"prompt": prompt_text, "tone": tone})
    
    return {
        "ai_pitch": response.content.strip(),
        "tone": tone
    }

# Evaluator Chain
def get_evaluation_result(prompt_text: str, human: str, ai: str, tone: str) -> dict:
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

    # trying to  parse JSON if gemini returns it, else fallback to text
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
