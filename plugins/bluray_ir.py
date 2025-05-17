import subprocess

def should_handle(query: str) -> bool:
    return any(word in query for word in ["blu-ray", "bluray", "disc", "movie"])

def handle(query: str) -> None:
    from core.stt_tts import speak

    if "play blu-ray" in query:
        subprocess.run(["ir-ctl", "-S", "bluray_play.ir"])
        speak("Playing Blu-ray disc.")
