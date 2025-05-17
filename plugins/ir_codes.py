import subprocess

def should_handle(query: str) -> bool:
    return any(word in query for word in ["turn on", "turn off", "volume"])

def handle(query: str) -> None:
    from core.stt_tts import speak

    # Example: Use ir-ctl (Linux) to send IR signals
    if "turn on soundbar" in query:
        subprocess.run(["ir-ctl", "-S", "soundbar_on.ir"])
        speak("Soundbar powered on.")
