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

# game State - Load prompts with fallback
if "prompt" not in st.session_state:
    try:
        with open("data/prompts.json") as f:
            prompts = json.load(f)
    except FileNotFoundError:
        # fallback prompts if file doesn't exist
        prompts = [
            {"prompt": "Create a social media post about sustainable living that would go viral"},
            {"prompt": "Write a compelling pitch for a new productivity app"},
            {"prompt": "Craft a motivational message for entrepreneurs facing failure"},
            {"prompt": "Market college washrooms as the best place for life decisions"},
            {"prompt": "Launch a startup that rents out fake friends for group projects"},
            {"prompt": "Create a dating app exclusively for people who hate small talk"}
        ]
    st.session_state.prompt = random.choice(prompts)

# init session state
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "ai_output" not in st.session_state:
    st.session_state.ai_output = ""
if "winner" not in st.session_state:
    st.session_state.winner = None
if "tone" not in st.session_state:
    st.session_state.tone = random.choice(["poetic", "sarcastic", "brandy", "inspirational", "humorous"])
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""

player = st.session_state.player_name

st.markdown(f"👋 Welcome, **{player}**!")
st.markdown(f"### 🎯 One-Shot Campaign Challenge")
st.info(f"**{st.session_state.prompt['prompt']}**")
st.markdown(f"🎙️ Tone of the Round: **{st.session_state.tone.upper()}**")

st.markdown("### 🎤 Record Your Pitch")
st.markdown("Click the microphone to start recording, click again to stop:")

wav_audio_data = st_audiorec()

# display transcribed text if available
if st.session_state.transcribed_text:
    st.markdown("### 📝 Your Transcribed Pitch:")
    st.text_area("Transcribed Text:", value=st.session_state.transcribed_text, height=100, disabled=True)

# process audio when recorded
if wav_audio_data is not None:
    st.audio(wav_audio_data, format="audio/wav")
    
    if st.button("🔄 Transcribe Audio", key="transcribe_recorded"):
        with st.spinner("🎧 Transcribing your pitch..."):
            try:
                # Save audio to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    tmp_file.write(wav_audio_data)
                    tmp_file.flush()  # Ensure data is written
                    tmp_file_path = tmp_file.name
                
                # Check if file was created successfully
                if os.path.exists(tmp_file_path) and os.path.getsize(tmp_file_path) > 0:
                    # Transcribe audio
                    transcribed_text = transcribe_audio_to_text(tmp_file_path)
                    
                    if transcribed_text and transcribed_text.strip():
                        st.session_state.transcribed_text = transcribed_text.strip()
                        st.session_state.user_input = transcribed_text.strip()
                        st.success("✅ Audio transcribed successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Could not transcribe audio. Please try speaking louder and clearer.")
                else:
                    st.error("❌ Failed to save audio file. Please try recording again.")
                
                # Clean up temporary file
                if 'tmp_file_path' in locals():
                    try:
                        os.unlink(tmp_file_path)
                    except:
                        pass
                
            except Exception as e:
                st.error(f"❌ Transcription failed: {str(e)}")
                st.info("💡 Try: Speaking clearly, avoiding background noise, or checking your Google Cloud setup")



# submit 
st.markdown("---")
if st.session_state.user_input:
    st.markdown("### ✅ Ready to Battle!")
    st.info(f"**Your pitch:** {st.session_state.user_input[:100]}{'...' if len(st.session_state.user_input) > 100 else ''}")
    
    if st.button("🚀 Battle the AI!", key="battle_ai"):
        with st.spinner("🤖 AI is crafting its response..."):
            try:
                # Call Writer
                writer_result = get_writer_response(
                    prompt_text=st.session_state.prompt["prompt"],
                    tone=st.session_state.tone
                )
                st.session_state.ai_output = writer_result["ai_pitch"]

                # Call Evaluator
                eval_result = get_evaluation_result(
                    prompt_text=st.session_state.prompt["prompt"],
                    human=st.session_state.user_input,
                    ai=writer_result["ai_pitch"],
                    tone=st.session_state.tone
                )
                
                st.session_state.eval_result = eval_result
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ AI battle failed: {str(e)}")
                st.info("🔧 Please check your API keys and internet connection")
else:
    st.markdown("### 🎤 Record or upload your audio pitch to continue!")

if st.session_state.ai_output:
    st.markdown("---")
    st.markdown("### AI's Response:")
    st.success(st.session_state.ai_output)

    st.markdown("### Judge's Verdict:")
    if hasattr(st.session_state, 'eval_result') and st.session_state.eval_result.get("verdict_text"):
        st.warning(st.session_state.eval_result["verdict_text"])
    


if st.session_state.ai_output:
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔁 Play Again", use_container_width=True):
            # Reset game state
            keys_to_reset = ["prompt", "user_input", "ai_output", "winner", "tone", "eval_result", "transcribed_text"]
            for key in keys_to_reset:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    with col2:
        if st.button("👤 Change Player", use_container_width=True):
            # Reset everything including player
            keys_to_reset = ["player_name", "prompt", "user_input", "ai_output", "winner", "tone", "eval_result", "transcribed_text"]
            for key in keys_to_reset:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# Instructions
with st.expander("📖 How to Use"):
    st.markdown("""
    ### 🎮 Game Flow:
    1. **Record Audio:** Click the microphone button to start/stop recording
    2. **Or Upload:** Choose an audio file from your device  
    3. **Transcribe:** Click the transcribe button to convert speech to text
    4. **Battle:** Hit the battle button to compete against AI
    5. **Enjoy:** See who wins the influence war!
    
    ### 🎤 Recording Tips:
    - Speak clearly and at normal pace
    - Avoid background noise
    - Keep recordings under 1 minute
    - Make sure your microphone is working
    
    ### 🏆 Winning Strategy:
    - Be creative and engaging
    - Match the tone of the round
    - Make it memorable and shareable
    """)

# Footer
st.markdown("---")
st.markdown("*Built with ❤️ for viral content creators*")