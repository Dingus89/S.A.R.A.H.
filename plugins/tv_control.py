import subprocess
import os
import requests
import time
from core.utils import parse_query
from core.stt_tts import speak
from core.cache_utils import get_cached_platform, set_cached_platform
from dotenv import load_dotenv

load_dotenv()
TMDB_KEY = os.getenv("TMDB_KEY")
ONN_DEVICE_IP = os.getenv("ONN_DEVICE_IP")
PLEX_SERVER = os.getenv("PLEX_SERVER")
PLEX_TOKEN = os.getenv("PLEX_TOKEN")

def should_handle(query: str) -> bool:
    return any(word in query for word in ["play", "watch", "stream", "netflix", "hulu", "tubi", "plex"])

def ensure_adb_connected():
    result = subprocess.run("adb devices", shell=True, capture_output=True)
    if ONN_DEVICE_IP not in result.stdout.decode():
        subprocess.run(f"adb connect {ONN_DEVICE_IP}", shell=True)
        time.sleep(1)
        return ONN_DEVICE_IP in subprocess.check_output("adb devices", shell=True).decode()
    return True

def tmdb_search(show):
    url = f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_KEY}&query={show}"
    try:
        response = requests.get(url).json()
        if response.get("results"):
            return response["results"][0]["id"], response["results"][0]["name"]
    except Exception:
        pass
    return None, show

def robust_adb_start(cmd, retries=3):
    for attempt in range(retries):
        result = subprocess.run(cmd, shell=True)
        if result.returncode == 0:
            return True
        time.sleep(1)
    return False

def justwatch_search(show_name):
    try:
        url = "https://apis.justwatch.com/content/titles/en_US/popular"
        response = requests.get(url, params={"query": show_name}, timeout=5).json()
        if not response:
            return None
        offers = response[0].get("offers", [])
        if not offers:
            return None
        for offer in offers:
            platform_id = offer.get("provider_id")
            if platform_id == 8: return "netflix"
            if platform_id == 15: return "hulu"
            if platform_id == 37: return "tubi"
        return None
    except Exception:
        return None

def plex_search_and_launch(show_name):
    try:
        headers = {'X-Plex-Token': PLEX_TOKEN}
        search_url = f"{PLEX_SERVER}/search?query={show_name}"
        response = requests.get(search_url, headers=headers).text
        if "<Video" in response or "<Directory" in response:
            speak(f"Launching {show_name} on Plex.")
            plex_launch = "adb shell monkey -p com.plexapp.android -c android.intent.category.LAUNCHER 1"
            return robust_adb_start(plex_launch)
        return False
    except Exception:
        return False

def launch_streaming_app(platform, show_name, show_id):
    if platform == "netflix":
        speak(f"Launching {show_name} on Netflix.")
        url = f"https://www.netflix.com/title/{show_id}"
        cmd = f"adb shell am start -a android.intent.action.VIEW -d '{url}'"
        return robust_adb_start(cmd)
    elif platform == "plex":
        return plex_search_and_launch(show_name)
    elif platform in ["tubi", "hulu"]:
        speak(f"Searching for {show_name} on {platform.title()}.")
        search_url = f"https://www.google.com/search?q={show_name}+{platform}+watch"
        cmd = f"adb shell am start -a android.intent.action.VIEW -d '{search_url}'"
        return robust_adb_start(cmd)
    return False

def handle(query: str) -> None:
    show, desc = parse_query(query)
    speak(f"Looking up {show}...")

    if not ensure_adb_connected():
        speak("Could not connect to ONN device.")
        return

    show_id, show_name = tmdb_search(show)
    if not show_id:
        speak(f"Could not find {show}.")
        return

    # Step 1: Try cache
    cached = get_cached_platform(show_name, season, episode)
if cached:
    platform = cached["platform"]
    show_id = cached.get("tmdb_id", show_id)
    speak(f"Found cached platform: {platform}.")
else:
    platform = justwatch_search(show_name)
    if platform:
        set_cached_platform(show_name, platform, tmdb_id=show_id, season=season, episode=episode)
        speak(f"Found {platform} via JustWatch.")
    else:
        speak("JustWatch could not find a platform. Checking Plex...")
        if plex_search_and_launch(show_name):
            set_cached_platform(show_name, "plex", tmdb_id=show_id, season=season,       
                episode=episode)
            else:
                speak("Falling back to Google search.")
                search_url = f"https://www.google.com/search?q={show_name}+watch+online"
                fallback_cmd = f"adb shell am start -a android.intent.action.VIEW -d '{search_url}'"
                robust_adb_start(fallback_cmd)
                return

    # Launch platform app
    success = launch_streaming_app(platform, show_name, show_id)
    if not success:
        speak(f"{platform.title()} failed. Trying Google search.")
        search_url = f"https://www.google.com/search?q={show_name}+{platform}+watch"
        fallback_cmd = f"adb shell am start -a android.intent.action.VIEW -d '{search_url}'"
        robust_adb_start(fallback_cmd)
