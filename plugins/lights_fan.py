import requests
import os
import subprocess
import paho.mqtt.publish as publish
from core.stt_tts import speak
from dotenv import load_dotenv

load_dotenv()

# Home Assistant config
HA_URL = os.getenv("HOME_ASSISTANT_URL")
HA_TOKEN = os.getenv("HOME_ASSISTANT_TOKEN")
HA_HEADERS = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}

# MQTT config
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USERNAME")
MQTT_PASS = os.getenv("MQTT_PASSWORD")
ZIGBEE_TOPIC = "zigbee2mqtt/livingroom_light"  # update this per device

# Matter CLI config
MATTER_NODE_ID = os.getenv("MATTER_NODE_ID", "1234")
MATTER_ENDPOINT = os.getenv("MATTER_LIGHT_ENDPOINT", "1")

def should_handle(query: str) -> bool:
    return any(word in query for word in [
        "light", "lamp", "bulb", "brightness",
        "color", "red", "blue", "green", "white", "yellow", "orange",
        "pink", "purple", "warm", "cool"
    ])

def handle(query: str) -> None:
    color = extract_color(query)
    if color:
        if set_color_ha(color) or set_color_mqtt(color):
            speak(f"Light color set to {color}.")
        else:
            speak(f"Failed to set color to {color}.")
        return

    if "turn on" in query:
        if control_ha(True) or control_mqtt(True) or control_matter(True):
            speak("Lights turned on.")
        else:
            speak("Failed to turn on the lights.")
    elif "turn off" in query:
        if control_ha(False) or control_mqtt(False) or control_matter(False):
            speak("Lights turned off.")
        else:
            speak("Failed to turn off the lights.")
    elif "brightness" in query:
        level = extract_brightness(query)
        if control_brightness_ha(level) or control_brightness_mqtt(level) or control_brightness_matter(level):
            speak(f"Brightness set to {level}.")
        else:
            speak("Failed to set brightness.")
    else:
        speak("I didn’t understand the light command.")

# -----------------------
# Control Functions
# -----------------------

def control_ha(state: bool) -> bool:
    try:
        entity = "light.linkind_bulb"
        url = f"{HA_URL}/api/services/light/turn_{'on' if state else 'off'}"
        response = requests.post(url, headers=HA_HEADERS, json={"entity_id": entity}, timeout=2)
        return response.status_code == 200
    except:
        return False

def control_brightness_ha(level: int) -> bool:
    try:
        entity = "light.linkind_bulb"
        url = f"{HA_URL}/api/services/light/turn_on"
        response = requests.post(url, headers=HA_HEADERS, json={"entity_id": entity, "brightness": level}, timeout=2)
        return response.status_code == 200
    except:
        return False

def set_color_ha(color: str) -> bool:
    try:
        entity = "light.linkind_bulb"
        url = f"{HA_URL}/api/services/light/turn_on"
        payload = {"entity_id": entity}

        if "white" in color:
            payload["color_temp"] = 250 if "warm" in color else 153
        else:
            payload["color_name"] = color

        response = requests.post(url, headers=HA_HEADERS, json=payload, timeout=2)
        return response.status_code == 200
    except:
        return False

def control_mqtt(state: bool) -> bool:
    try:
        payload = {"state": "ON" if state else "OFF"}
        publish.single(ZIGBEE_TOPIC, payload=str(payload).replace("'", '"'),
                       hostname=MQTT_BROKER, port=MQTT_PORT,
                       auth={"username": MQTT_USER, "password": MQTT_PASS})
        return True
    except:
        return False

def control_brightness_mqtt(level: int) -> bool:
    try:
        payload = {"state": "ON", "brightness": level}
        publish.single(ZIGBEE_TOPIC, payload=str(payload).replace("'", '"'),
                       hostname=MQTT_BROKER, port=MQTT_PORT,
                       auth={"username": MQTT_USER, "password": MQTT_PASS})
        return True
    except:
        return False

def set_color_mqtt(color: str) -> bool:
    try:
        payload = {"state": "ON"}
        if "white" in color:
            payload["color_temp"] = 250 if "warm" in color else 153
        else:
            payload["color"] = {"name": color}

        publish.single(ZIGBEE_TOPIC, payload=str(payload).replace("'", '"'),
                       hostname=MQTT_BROKER, port=MQTT_PORT,
                       auth={"username": MQTT_USER, "password": MQTT_PASS})
        return True
    except:
        return False

def control_matter(state: bool) -> bool:
    try:
        cmd = f"chip-tool onoff {'on' if state else 'off'} {MATTER_NODE_ID} {MATTER_ENDPOINT}"
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except:
        return False

def control_brightness_matter(level: int) -> bool:
    try:
        cmd = f"chip-tool levelcontrol move-to-level {level} 0 0 0 {MATTER_NODE_ID} {MATTER_ENDPOINT}"
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except:
        return False

# -----------------------
# Utilities
# -----------------------

def extract_brightness(query: str) -> int:
    if "100" in query: return 254
    if "75" in query: return 191
    if "50" in query: return 127
    if "25" in query: return 63
    return 200

def extract_color(query: str) -> str:
    colors = ["red", "blue", "green", "white", "yellow", "orange", "pink", "purple", "warm white", "cool white"]
    for color in colors:
        if color in query.lower():
            return color
    return None
