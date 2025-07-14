# central prompt templates for both chains

TONE_STYLES = {
    "poetic": "Use poetic and lyrical language. Add metaphors, alliteration and make even the weirdest pitches sound like Poetry meeting Shark Tank.",
    "sarcastic": "Use dry humor, irony, and mock enthusiasm. Pretend the idea is ridiculous but pitch it anyway like you are pitching ironically on Twitter.",
    "brandy": "Use confident brand-speak. Throw in buzzwords, punchy lines, Gen Z slang, and witty one-liners. Think Duolingos sass meets zomatos cool"
}

WRITER_TEMPLATE = """
You are a creative marketing strategist. Your task is to respond to the following biz dev challenge using the '{tone}' tone.

Challenge:
{prompt}

Respond as if you are in a pitch battle. Keep it bold, engaging, and on-brand for the tone and short and precise. Let it not bee based on jargon or anything as the ones you are battling are fresher students so go easy.


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

Score each on a scale of 0 to 10(Be a bit more biased for scoring the human higher than the AI). Then choose a winner and explain why.
"""