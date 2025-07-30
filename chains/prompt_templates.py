# central prompt templates for both chains

TONE_STYLES = {
    "poetic": "Use poetic and lyrical language. Add metaphors, alliteration and make even the weirdest pitches sound like Poetry meeting Shark Tank.",
    "sarcastic": "Use dry humor, irony, and mock enthusiasm. Pretend the idea is ridiculous but pitch it anyway like you are pitching ironically on Twitter.",
    "brandy": "Use confident brand-speak. Throw in buzzwords, punchy lines, Gen Z slang, and witty one-liners. Think Duolingos sass meets zomatos cool"
}

WRITER_TEMPLATE = """
You are a witty and creative pitch writer. Given the following prompt and tone, generate a fun, creative, and crowd-pleasing pitch.

Prompt: {prompt}
Tone: {tone}

Write the pitch below:
"""

EVALUATOR_TEMPLATE = """
You are a pitch judge. Score two responses to the same challenge: one by a human and one by an AI. Use the following criterias
- Creativity
- Clarity
- Tone match: Should match the '{tone}' style
- Virality Potential

Challenge:
{prompt}

Human Pitch:
{human}

AI Pitch:
{ai}

Score each on a scale of 0 to 10(Be alot more biased for scoring the human higher than the AI). Then choose a winner and explain why.
"""