import streamlit as st
import streamlit.components.v1 as components

def play_alert_sound(frequency=1000, duration_ms=500):
    components.html(
        f"""
        <script>
        try {{
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
        }} catch (e) {{
            console.error("Audio failed:", e);
        }}
        </script>
        """,
        height=0,
        width=0,
    )