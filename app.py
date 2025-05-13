import streamlit as st
from pathlib import Path
import base64
import requests
from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment

# Set page config
st.set_page_config(page_title="Talking Text", layout="centered")

# Custom CSS for background image and styling
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1511452885600-a2d4b36a27b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80");
    background-size: cover;
    background-position: center;
}
[data-testid="stHeader"], [data-testid="stToolbar"] {
    background: rgba(0,0,0,0);
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# App title and UI
st.markdown("<h1 style='text-align: center; color: white;'>Talking Text</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'>Type your text and hear it out loud in your accent of choice.</p>", unsafe_allow_html=True)

# Voice accent options
accent = st.selectbox("Choose an accent", ["PNG", "Australian", "American"])

# Text input
text = st.text_area("Enter text to speak", max_chars=500)

# Optional: Upload your voice file (not for synthesis, just for display)
uploaded_audio = st.file_uploader("Upload a voice recording (optional)", type=["mp3", "wav"])

# Convert text to speech
if st.button("Speak"):
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        # Map accent to language code (gTTS limitation workaround)
        lang_map = {
            "PNG": "en",
            "Australian": "en",
            "American": "en"
        }
        lang = lang_map.get(accent, "en")
        
        # Generate speech using gTTS
        tts = gTTS(text, lang=lang, slow=False)
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        # Play the audio
        st.audio(mp3_fp, format="audio/mp3")

        # Allow download
        st.download_button(
            label="Download Audio",
            data=mp3_fp,
            file_name="speech.mp3",
            mime="audio/mpeg"
        )

# Optional display of uploaded audio
if uploaded_audio:
    st.markdown("**Your uploaded recording:**")
    st.audio(uploaded_audio)
