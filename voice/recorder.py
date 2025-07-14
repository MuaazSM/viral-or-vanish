import streamlit as st
from audio_recorder_streamlit import audio_recorder

def record_audio():
    st.markdown("🎤 **Speak your pitch out loud below:**")
    audio_bytes = audio_recorder()
    return audio_bytes