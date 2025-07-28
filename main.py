import streamlit as st
import random
import json
from datetime import datetime
from chains.llm_handler import get_writer_response, get_evaluation_result
from utils.prompt_selector import get_random_prompt

# Config
st.set_page_config(page_title="Viral or Vanish", page_icon="🔥", layout="centered")

# Title
st.title("🔥 Viral or Vanish: Influence War")
st.subheader("Pitch like a legend. Battle the AI. Win the crowd.")
st.markdown("---")

# Player Name
if "player_name" not in st.session_state:
    st.session_state.player_name = ""

if st.session_state.player_name == "":
    st.markdown("### Enter your name to begin the influence war 👇")
    name_input = st.text_input("Your Name", placeholder="e.g., Muaaz")

    if st.button("Start Game 🚀") and name_input.strip():
        st.session_state.player_name = name_input.strip()
        st.rerun()
    st.stop()

# Game State
if "prompt" not in st.session_state:
    # with open("data/prompts.json") as f:
    #     prompts = json.load(f)
    #     st.session_state.prompt = random.choice(prompts)
    st.session_state.prompt = get_random_prompt()

if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "ai_output" not in st.session_state:
    st.session_state.ai_output = ""
if "winner" not in st.session_state:
    st.session_state.winner = None
if "tone" not in st.session_state:
    st.session_state.tone = random.choice(["poetic", "sarcastic", "brandy"])

player = st.session_state.player_name

# Greet + Prompt
st.markdown(f"👋 Welcome, **{player}**!")
st.markdown(f"### 🎯 One-Shot Campaign Challenge")
st.info(f"**{st.session_state.prompt['prompt']}**")
st.markdown(f"🎙️ Tone of the Round: **{st.session_state.tone.upper()}**")

# Caption Input Form
with st.form(key="pitch_form"):
    user_input = st.text_area("✍️ Your Pitch:", value=st.session_state.user_input, height=150)
    submit_btn = st.form_submit_button("🚀 Submit")

# On Submit
if submit_btn:
    st.session_state.user_input = user_input
    st.markdown("✅ Pitch locked in. The AI is responding...")

    # Call Writer
    writer_result = get_writer_response(
        prompt_text=st.session_state.prompt["prompt"],
        tone=st.session_state.tone
    )
    st.session_state.ai_output = writer_result["ai_pitch"]

    # Call Evaluator
    eval_result = get_evaluation_result(
        prompt_text=st.session_state.prompt["prompt"],
        human=user_input,
        ai=writer_result["ai_pitch"],
        tone=st.session_state.tone
    )

    # Display AI response
    st.markdown("### 🤖 AI’s Response:")
    st.success(writer_result["ai_pitch"])

    # Display Verdict
    st.markdown("### 🧠 Judge’s Verdict:")
    if eval_result.get("verdict_text"):
        st.warning(eval_result["verdict_text"])

    # Emoji Feedback
    st.markdown("### 🎭 Audience Reaction:")
    st.markdown("😱👏🔥 *Crowd goes wild... or does it?*")

    # Leaderboard Save
    # import pandas as pd
    # entry = {
    #     "player": player,
    #     "prompt": st.session_state.prompt["prompt"],
    #     "tone": st.session_state.tone,
    #     "player_pitch": user_input,
    #     "ai_pitch": writer_result["ai_pitch"],
    #     "verdict": eval_result.get("verdict_text"),
    #     "timestamp": datetime.now().isoformat()
    # }
    # df = pd.DataFrame([entry])
    # df.to_csv("data/leaderboard.csv", mode="a", header=False, index=False)

# Play Again
if st.session_state.ai_output:
    st.markdown("---")
    if st.button("🔁 Play Again"):
        for key in ["prompt", "user_input", "ai_output", "winner", "tone"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()