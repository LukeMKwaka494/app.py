import streamlit as st import requests import base64 import os from streamlit.components.v1 import html

App config

st.set_page_config(page_title="Talking Text AI", layout="centered")

Custom CSS for styling

st.markdown(""" <style> body { background-image: url('https://images.unsplash.com/photo-1525286116112-b59af11adad1'); background-size: cover; } .main { background: rgba(255, 255, 255, 0.8); padding: 2em; border-radius: 15px; } .stTextInput>div>div>input { font-size: 18px; color: #333; border-radius: 10px; } .stButton button { border-radius: 10px; background-color: #00bfff; color: white; } audio { width: 100%; } </style> """, unsafe_allow_html=True)

Header

st.markdown("<h1 style='text-align: center; color: #00bfff;'>Talking Text AI</h1>", unsafe_allow_html=True)

Input form

st.markdown("### Enter your message:") user_input = st.text_area("Text to convert to speech", height=150, max_chars=500)

Voice options

voice = st.selectbox("Select Voice", ["PNG Male", "PNG Female", "Neutral Male", "Neutral Female"])

Submit button

if st.button("Convert to Voice"): if user_input.strip() == "": st.warning("Please enter text to convert.") else: # Display loading spinner with st.spinner("Generating voice..."): voice_id_map = { "PNG Male": "mf7tG5zFUkp8ZjibWqsw", "PNG Female": "mYslTkfVThZ6y6EF1J2T", "Neutral Male": "pNInz6obpgDQGcFmaJgB", "Neutral Female": "EXAVITQu4vr4xnSDxMaL" } voice_id = voice_id_map.get(voice, "EXAVITQu4vr4xnSDxMaL")

CHUNK_SIZE = 1024
        headers = {
            "xi-api-key": st.secrets["ELEVENLABS_API_KEY"],
            "Content-Type": "application/json"
        }

        payload = {
            "text": user_input,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.7,
                "similarity_boost": 0.5
            }
        }

        try:
            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                headers=headers,
                json=payload
            )
            if response.status_code == 200:
                audio_path = "/mnt/data/output.mp3"
                with open(audio_path, 'wb') as f:
                    f.write(response.content)

                st.audio(audio_path, format="audio/mp3")

                # Animate waveform using HTML canvas
                html("""
                <script>
                const canvas = document.createElement('canvas');
                canvas.width = 500;
                canvas.height = 100;
                const ctx = canvas.getContext('2d');
                document.body.appendChild(canvas);
                let i = 0;
                function draw() {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    for (let x = 0; x < canvas.width; x++) {
                        let y = 50 + Math.sin((x + i) * 0.05) * 20;
                        ctx.fillRect(x, y, 1, 1);
                    }
                    i++;
                    requestAnimationFrame(draw);
                }
                draw();
                </script>
                """, height=120)

                # Download link
                with open(audio_path, "rb") as file:
                    btn = st.download_button(
                        label="Download Audio",
                        data=file,
                        file_name="talking_text.mp3",
                        mime="audio/mp3"
                    )
            else:
                st.error("Error: Could not generate audio.")

        except Exception as e:
            st.error(f"Exception: {e}")

Footer

st.markdown(""" <hr> <p style='text-align:center;'>Created with love for PNG | <strong>Talking Text AI</strong></p> """, unsafe_allow_html=True)

