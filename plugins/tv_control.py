import os
import requests
import time
from dotenv import load_dotenv
from core.utils import parse_query
from core.stt_tts import speak
from cache_utils import get_cached_platform, set_cached_platform

load_dotenv()

TMDB_KEY = os.getenv("TMDB_KEY")
PLEX_TOKEN = os.getenv("PLEX_TOKEN")
PLEX_SERVER = os.getenv("PLEX_SERVER")
ONN_IP = os.getenv("ONN_DEVICE_IP")
ADB_PATH = "adb"  # Adjust if installed elsewhere

def should_handle(query: str) -> bool:
    return any(word in query.lower() for word in ["watch", "play", "stream", "episode", "season"])

def handle(query: str) -> None:
    show, season, episode = parse_query(query)
    if not show:
        speak("I didn't catch which show you want.")
        return

    show_id, show_name = tmdb_search(show)
    if not show_id:
        speak("I couldn't find that show in the database.")
        return

    cached = get_cached_platform(show_name, season, episode)
    if cached:
        platform = cached["platform"]
        show_id = cached.get("tmdb_id", show_id)
        speak(f"Found cached platform: {platform}.")
    else:
        platform = justwatch_search(show_name)
        if platform:
            speak(f"I found {show_name} on {platform}.")
            set_cached_platform(show_name, platform, tmdb_id=show_id, season=season, episode=episode)
        else:
            speak("JustWatch couldn't find it. Trying Plex...")
            if plex_search_and_launch(show_name):
                set_cached_platform(show_name, "plex", tmdb_id=show_id, season=season, episode=episode)
                return
            speak("I couldn’t find that show on your platforms.")
            return

    if platform == "plex":
        plex_search_and_launch(show_name)
        return

    launch_to_platform(platform, show_name, season, episode)

# === TMDB ===
def tmdb_search(show_name):
    try:
        url = f"https://api.themoviedb.org/3/search/tv?query={show_name}&api_key={TMDB_KEY}"
        response = requests.get(url).json()
        results = response.get("results", [])
        if results:
            show_id = results[0]["id"]
            name = results[0]["name"]
            return show_id, name
    except Exception as e:
        print(f"[TMDB error] {e}")
    return None, show_name

# === JustWatch / Google ===
def justwatch_search(show_name):
    try:
        url = f"https://www.google.com/search?q=watch+{show_name.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers).text.lower()
        for platform in ["netflix", "hulu", "tubi", "amazon", "disney+", "prime", "hbo", "paramount"]:
            if platform in r:
                return platform
    except Exception as e:
        print(f"[JustWatch/Google error] {e}")
    return None

# === Plex ===
def plex_search_and_launch(show_name):
    try:
        url = f"{PLEX_SERVER}/search?query={show_name}"
        headers = {"X-Plex-Token": PLEX_TOKEN}
        r = requests.get(url, headers=headers)
        if r.status_code == 200 and show_name.lower() in r.text.lower():
            os.system(f'xdg-open "{PLEX_SERVER}/web/index.html#!/search?query={show_name}"')
            speak(f"Playing {show_name} on Plex.")
            return True
    except Exception as e:
        print(f"[Plex error] {e}")
    return False

# === ADB Control ===
def adb(cmd):
    full = f"{ADB_PATH} -s {ONN_IP}:5555 {cmd}"
    print(f"[ADB] {full}")
    os.system(full)

def connect_adb():
    os.system(f"{ADB_PATH} connect {ONN_IP}:5555")
    time.sleep(1)

def launch_to_platform(platform, show, season=None, episode=None):
    try:
        connect_adb()
        platform = platform.lower()

        if platform == "netflix":
            adb("shell monkey -p com.netflix.ninja -c android.intent.category.LAUNCHER 1")
        elif platform == "tubi":
            adb("shell monkey -p com.tubitv -c android.intent.category.LAUNCHER 1")
        elif platform == "youtube":
            adb("shell monkey -p com.google.android.youtube.tv -c android.intent.category.LAUNCHER 1")
        elif platform == "amazon" or platform == "prime":
            adb("shell monkey -p com.amazon.avod.thirdpartyclient -c android.intent.category.LAUNCHER 1")
        elif platform == "hulu":
            adb("shell monkey -p com.hulu.plus -c android.intent.category.LAUNCHER 1")
        elif platform == "disney+":
            adb("shell monkey -p com.disney.disneyplus -c android.intent.category.LAUNCHER 1")
        else:
            speak(f"I don’t support ADB control for {platform} yet.")
            return

        time.sleep(2)
        adb("shell input keyevent 84")  # KEYCODE_SEARCH

        query = show
        if season and episode:
            query += f" season {season} episode {episode}"

        adb(f'shell input text "{query}"')
        time.sleep(1)
        adb("shell input keyevent 66")  # KEYCODE_ENTER

        speak(f"Searching for {show} on {platform}.")
    except Exception as e:
        print(f"[ADB error] {e}")
        speak("I had trouble sending commands to the TV.")