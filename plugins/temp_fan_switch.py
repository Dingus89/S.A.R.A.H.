import asyncio
import websockets
import os
from core.stt_tts import speak
from dotenv import load_dotenv

load_dotenv()
WS_URL = os.getenv("ESP32_WS_URL")

RELAY_MAP = {
    "light": "L",
    "fan low": "1",
    "fan medium": "2",
    "fan high": "3",
    "fan off": "0"
}

def should_handle(query: str) -> bool:
    return any(k in query.lower() for k in RELAY_MAP)

def handle(query: str) -> None:
    for keyword, code in RELAY_MAP.items():
        if keyword in query.lower():
            try:
                asyncio.run(send_ws_command(code))
                speak(f"{keyword.capitalize()} activated.")
                return
            except Exception as e:
                speak("Could not reach the fan system.")
                print(f"WebSocket error: {e}")
                return
    speak("I didn’t understand the fan command.")

async def send_ws_command(code):
    async with websockets.connect(WS_URL) as ws:
        await ws.send(code)
