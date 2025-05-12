import streamlit as st
import asyncio
import edge_tts
import os

# Set page title
st.set_page_config(page_title="Talking Text: PNG Text-to-Speech")

# Set background image
background_url = "https://raw.githubusercontent.com/LukeMKwaka494/app.py/main/BackgroundEraser_20250504_094053758.png"
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# App title and instructions
st.title("Talking Text: PNG Text-to-Speech")
st.write("Write something in English or Tok Pisin, and this app will speak it for you.")

# User input
user_text = st.text_area("Enter your text here:")

# Voice selection
voice_option = st.selectbox("Choose a voice:", [
    "en-AU-WilliamNeural",  # Australian Male
    "en-AU-AnnetteNeural",  # Australian Female
    "en-GB-RyanNeural",     # British Male
    "en-US-JennyNeural"     # American Female
])

# Speak button
if st.button("Speak"):
    if user_text.strip():
        async def speak():
            tts = edge_tts.Communicate(user_text, voice_option)
            await tts.save("output.mp3")

        asyncio.run(speak())

        # Play the audio
        with open("output.mp3", "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")

        os.remove("output.mp3")
    else:
        st.warning("Please enter some text first.")
