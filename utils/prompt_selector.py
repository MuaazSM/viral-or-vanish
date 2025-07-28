# Random prompt selection logic
import json
import random
from typing import Dict, Any

PROMPTS_PATH = "data/prompts.json"

def load_prompts() -> list[Dict[str, Any]]:
    """Load all prompts from the prompts.json file."""
    with open(PROMPTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_random_prompt() -> Dict[str, Any]:
    """Return a random prompt dictionary from the prompts list."""
    prompts = load_prompts()
    return random.choice(prompts)

