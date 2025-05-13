import streamlit as st
import requests
import base64

# Page config

st.set_page_config(page_title="Talking Text", page_icon="📢", layout="centered")


# Custom CSS
st.markdown("""
    <style>
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
st.markdown("## 📢 Talking Text")
st.write("Type your text and hear it spoken in a natural voice. PNG accent available.")

# Voice options (replace with real voice IDs from ElevenLabs)
voice_options = {
    "Default (US English)": "EXAVITQu4vr4xnSDxMaL",
    "Papua New Guinea Style (Closest Match)": "your_custom_voice_id_here"
}
voice_choice = st.selectbox("Choose a voice", list(voice_options.keys()))
voice_id = voice_options[voice_choice]

# API Key
api_key = st.secrets.get("elevenlabs_api_key") or st.text_input("Enter your ElevenLabs API Key", type="password")

# Chat-style input
user_input = st.chat_input("Type something to say...")

# Process input
if user_input and api_key:
    with st.spinner("Generating audio..."):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
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

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            audio = response.content

            st.markdown(f'<div class="chat-bubble">{user_input}</div>', unsafe_allow_html=True)
            st.markdown('<div class="wave-placeholder"></div>', unsafe_allow_html=True)
            st.audio(audio, format="audio/mp3")
            st.download_button("Download Audio", audio, file_name="talking_text.mp3")

        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
else:
    if not api_key:
        st.info("Please enter your ElevenLabs API key above to continue.")
