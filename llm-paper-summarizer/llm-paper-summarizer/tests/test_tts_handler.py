from utils.tts_handler import generate_audio
import os

def test_tts_handler():
    audio_path = generate_audio("Test audio")
    assert not audio_path.startswith("Error")
    assert os.path.exists(audio_path)