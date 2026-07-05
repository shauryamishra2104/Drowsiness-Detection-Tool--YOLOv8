import streamlit as st
import numpy as np
import io
import wave

def generate_beep(frequency=1000, duration_ms=500, sample_rate=44100):
    t = np.linspace(0, duration_ms / 1000, int(sample_rate * duration_ms / 1000), False)
    tone = np.sin(frequency * t * 2 * np.pi)
    audio = (tone * 32767 / np.max(np.abs(tone))).astype(np.int16)

    buffer = io.BytesIO()
    with wave.open(buffer, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    buffer.seek(0)
    return buffer

def play_alert_sound(frequency=1000, duration_ms=500):
    audio_buffer = generate_beep(frequency, duration_ms)
    st.audio(audio_buffer, format="audio/wav", autoplay=True)