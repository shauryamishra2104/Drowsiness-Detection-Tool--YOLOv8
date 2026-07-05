import streamlit as st
import streamlit.components.v1 as components

def play_alert_sound(frequency=1000, duration_ms=500):
    """Plays a beep in the browser using Web Audio API. Call this once per alert trigger."""
    components.html(
        f"""
        <script>
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = ctx.createOscillator();
        const gainNode = ctx.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(ctx.destination);
        oscillator.frequency.value = {frequency};
        oscillator.type = "sine";
        gainNode.gain.setValueAtTime(0.3, ctx.currentTime);
        oscillator.start();
        oscillator.stop(ctx.currentTime + {duration_ms / 1000});
        </script>
        """,
        height=0,
        width=0,
    )