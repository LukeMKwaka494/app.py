import streamlit as st
import requests
import base64
import time

# Set page config
st.set_page_config(page_title="Talking Text", page_icon="🗣️", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        body {
            background-color: #f0f2f6;
        }
        .chat-bubble {
            background-color: #e1f5fe;
            padding: 10px 15px;
            border-radius: 20px;
            margin: 10px 0;
            max-width: 80%;
        }
        .wave-placeholder {
            width: 100%;
            height: 40px;
            background: linear-gradient(90deg, #0099ff, #33ccff);
            animation: wave 1.5s infinite ease-in-out;
        }
        @keyframes wave {
            0% {opacity: 0.3;}
            50% {opacity: 1;}
            100% {opacity: 0.3;}
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("## 🗣️ Talking Text")
st.write("Type your text and hear it spoken in a natural voice. PNG accent available.")

# Voice options
voice_options = {
    "Default (US English)": "Rachel",
    "Papua New Guinea Style (Closest Match)": "Matilda"  # Replace with your own voice ID if needed
}
voice_choice = st.selectbox("Choose a voice", list(voice_options.keys()))
voice_id = voice_options[voice_choice]

# ElevenLabs API setup
api_key = st.secrets.get("elevenlabs_api_key") or st.text_input("Enter your ElevenLabs API Key", type="password")

# Chat-style input
user_input = st.chat_input("Type something to say...")

if user_input and api_key:
    with st.spinner("Generating audio..."):
        # Call ElevenLabs API
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }
        data = {
            "text": user_input,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            audio = response.content
            audio_b64 = base64.b64encode(audio).decode("utf-8")

            # Show chat bubble
            st.markdown(f'<div class="chat-bubble">{user_input}</div>', unsafe_allow_html=True)

            # Show soundwave animation placeholder
            st.markdown('<div class="wave-placeholder"></div>', unsafe_allow_html=True)

            # Play and download audio
            st.audio(audio, format="audio/mp3")
            st.download_button("Download Audio", audio, file_name="talking_text.mp3")
        else:
            st.error("Something went wrong. Please check your API key or try again later.")

elif not api_key:
    st.info("Please enter your ElevenLabs API key above to continue.")
