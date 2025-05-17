import requests

def should_handle(query: str) -> bool:
    return any(word in query for word in ["coffee", "brew", "caffeine"])

def handle(query: str) -> None:
    from core.stt_tts import speak

    # Example: Smarter Coffee API
    if "make coffee" in query:
        requests.post(
            "http://smarter-coffee-maker/brew",
            params={"cups": 1}
        )
        speak("Brewing 1 cup of coffee.")
