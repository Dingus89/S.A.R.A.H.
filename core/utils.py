import requests
import json
from core.llm import llm

def parse_query(query):
    prompt = f"""Extract show, season, and episode from:
Query: {query}
Respond ONLY with: "Show: [name]; Season: [num]; Episode: [num]" or "Show: [name]" if unknown.
Response:"""

    try:
        response = llm(prompt, max_tokens=50)
        text = response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[Parse Error] {e}")
        return None, None, None

    show, season, episode = None, None, None
    parts = text.strip().split("; ")
    for part in parts:
        if part.lower().startswith("show:"):
            show = part.split(":")[1].strip()
        elif part.lower().startswith("season:"):
            season = part.split(":")[1].strip()
        elif part.lower().startswith("episode:"):
            episode = part.split(":")[1].strip()

    return show, season, episode
def find_platform(show):
    with open("../configs/platform_priority.json") as f:
        priority = json.load(f)
    
    for platform in priority.get(show.lower(), ["plex", "netflix", "tubi"]):
        if check_platform_availability(show, platform):
            return platform
    return None

def check_platform_availability(show, platform):
    # Mock: Replace with JustWatch API or Plex library scan
    return True
