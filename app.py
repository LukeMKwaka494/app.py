import streamlit as st
from gtts import gTTS

# Set page info
st.set_page_config(page_title="Talking Text", page_icon="🗣️")

# App Header
st.title("**Talking Text: PNG Text-to-Speech**")
st.write("Write something in English or Tok Pisin, and this app will speak it for you.")

# Input field
text = st.text_area("Enter your text here:", height=150)
lang = st.selectbox("Choose Language", ["English", "Tok Pisin"])
lang_code = "en" if lang == "English" else "tpi"

# Speak Button
if st.button("Speak"):
    if text.strip() != "":
        tts = gTTS(text=text, lang=lang_code)
        tts.save("output.mp3")
        st.audio("output.mp3", format="audio/mp3")
    else:
        st.warning("Please enter some text first.")
