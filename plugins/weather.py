import requests

def should_handle(query: str) -> bool:
    return any(word in query for word in ["weather", "forecast", "temperature"])

def handle(query: str) -> None:
    from core.stt_tts import speak
    
    # Example: NWS API (free)
    response = requests.get(
        "https://api.weather.gov/gridpoints/TOP/31,80/forecast"
    ).json()
    forecast = response["properties"]["periods"][0]["detailedForecast"]
    
    speak(f"Weather report: {forecast}")
