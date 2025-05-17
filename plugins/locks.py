import requests

def should_handle(query: str) -> bool:
    return any(word in query for word in ["lock", "unlock", "door"])

def handle(query: str) -> None:
    from core.stt_tts import speak

    # Example: August Lock API
    if "unlock front door" in query:
        requests.put(
            "https://api.august.com/locks/12345/unlock",
            headers={"Authorization": "Bearer YOUR_TOKEN"}
        )
        speak("Front door unlocked.")
