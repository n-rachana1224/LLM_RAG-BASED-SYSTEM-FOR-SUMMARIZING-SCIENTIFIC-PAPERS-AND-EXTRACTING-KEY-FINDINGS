from gtts import gTTS
import os

def generate_audio(text):
    """Convert text to audio and save as MP3."""
    try:
        tts = gTTS(text=text, lang='en')
        audio_path = "data\\test_outputs\\output.mp3"
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        return f"Error generating audio: {e}"