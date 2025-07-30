import streamlit as st
import random
import json
import tempfile
import os
from datetime import datetime
from chains.llm_handler import get_writer_response, get_evaluation_result, transcribe_audio_to_text
from st_audiorec import st_audiorec

st.set_page_config(page_title="Viral or Vanish", page_icon="🔥", layout="centered")

st.title("🔥 Viral or Vanish: Influence War")
st.subheader("Pitch like a legend. Battle the AI. Win the crowd.")
st.markdown("---")

if "player_name" not in st.session_state:
    st.session_state.player_name = ""

if st.session_state.player_name == "":
    st.markdown("### Enter your name to begin the influence war 👇")
    name_input = st.text_input("Your Name", placeholder="e.g., Muaaz")

    if st.button("Start Game") and name_input.strip():
        st.session_state.player_name = name_input.strip()
        st.rerun()
    st.stop()

# Load prompt
if "prompt" not in st.session_state:
    try:
        with open("data/prompts.json") as f:
            prompts = json.load(f)
    except FileNotFoundError:
        prompts = [{"prompt": "Create a social media post about sustainable living that would go viral"}]
    st.session_state.prompt = random.choice(prompts)

# Init session
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "ai_output" not in st.session_state:
    st.session_state.ai_output = ""
if "winner" not in st.session_state:
    st.session_state.winner = None
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""

player = st.session_state.player_name

st.markdown(f"👋 Welcome, **{player}**!")
st.markdown("### 🎯 One-Shot Campaign Challenge")
st.success(f"**{st.session_state.prompt['prompt']}**")

st.markdown("### 🎤 Record Your Pitch")
st.markdown("Click the microphone to start recording, click again to stop:")

wav_audio_data = st_audiorec()

if st.session_state.transcribed_text:
    st.markdown("### 📝 Your Transcribed Pitch:")
    st.text_area("Transcribed Text:", value=st.session_state.transcribed_text, height=100, disabled=True)

if wav_audio_data is not None:
    st.audio(wav_audio_data, format="audio/wav")
    
    if st.button("🔄 Transcribe Audio", key="transcribe_recorded"):
        with st.spinner("🎧 Transcribing your pitch..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    tmp_file.write(wav_audio_data)
                    tmp_file_path = tmp_file.name

                if os.path.exists(tmp_file_path) and os.path.getsize(tmp_file_path) > 0:
                    transcribed_text = transcribe_audio_to_text(tmp_file_path)
                    if transcribed_text and transcribed_text.strip():
                        st.session_state.transcribed_text = transcribed_text.strip()
                        st.session_state.user_input = transcribed_text.strip()
                        st.success("✅ Audio transcribed successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Could not transcribe audio. Please try again.")
                else:
                    st.error("❌ Failed to save audio file.")

                if 'tmp_file_path' in locals():
                    try: os.unlink(tmp_file_path)
                    except: pass

            except Exception as e:
                st.error(f"❌ Transcription failed: {str(e)}")

# Battle UI
st.markdown("---")
if st.session_state.user_input:
    st.markdown("### ✅ Ready to Battle!")
    st.info(f"**Your pitch:** {st.session_state.user_input[:100]}{'...' if len(st.session_state.user_input) > 100 else ''}")
    
    if st.button("🚀 Battle the AI!", key="battle_ai"):
        with st.spinner("🤖 AI is crafting its response..."):
            try:
                writer_result = get_writer_response(prompt_text=st.session_state.prompt["prompt"])
                st.session_state.ai_output = writer_result["ai_pitch"]

                eval_result = get_evaluation_result(
                    prompt_text=st.session_state.prompt["prompt"],
                    human=st.session_state.user_input,
                    ai=writer_result["ai_pitch"]
                )
                st.session_state.eval_result = eval_result
                st.rerun()
            except Exception as e:
                st.error(f"❌ AI battle failed: {str(e)}")

else:
    st.markdown("### 🎤 Record or upload your audio pitch to continue!")

if st.session_state.ai_output:
    st.markdown("---")
    st.markdown("### 🤖 AI's Response:")
    st.success(st.session_state.ai_output)

    st.markdown("### 🧑‍⚖️ Judge's Verdict:")
    if st.session_state.eval_result.get("verdict_text"):
        st.warning(st.session_state.eval_result["verdict_text"])

# End-of-round buttons
if st.session_state.ai_output:
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔁 Play Again", use_container_width=True):
            keys_to_reset = ["prompt", "user_input", "ai_output", "winner", "eval_result", "transcribed_text"]
            for key in keys_to_reset:
                st.session_state.pop(key, None)
            st.rerun()

    with col2:
        if st.button("👤 Change Player", use_container_width=True):
            keys_to_reset = ["player_name", "prompt", "user_input", "ai_output", "winner", "eval_result", "transcribed_text"]
            for key in keys_to_reset:
                st.session_state.pop(key, None)
            st.rerun()

# Instructions
with st.expander("📖 How to Use"):
    st.markdown("""
    ### 🎮 Game Flow:
    1. **Record Audio:** Click the microphone to start/stop recording
    2. **Transcribe:** Click the transcribe button
    3. **Battle:** Hit the battle button to compete against AI
    4. **Enjoy:** See who wins the pitch war!

    ### 🎤 Tips:
    - Keep it fun, short, and creative
    - No need to be serious — make the judges laugh
    """)

# Footer
st.markdown("---")
st.markdown("*Built with ❤️ for viral pitches*")
