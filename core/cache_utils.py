import json
import os
import time

CACHE_FILE = "configs/show_platform_cache.json"
EXPIRATION_SECONDS = 60 * 60 * 24 * 7  # 7 days

def load_platform_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

def save_platform_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def get_cached_platform(show_name, season=None, episode=None):
    cache = load_platform_cache()
    entry = cache.get(show_name.lower())
    if not entry:
        return None

    # Per-episode entry?
    if season and episode:
        ep_key = f"s{season}e{episode}"
        ep_entry = entry.get("episodes", {}).get(ep_key)
        if ep_entry and time.time() - ep_entry.get("timestamp", 0) < EXPIRATION_SECONDS:
            return ep_entry

    # Fallback to show-level
    if time.time() - entry.get("timestamp", 0) < EXPIRATION_SECONDS:
        return entry
    return None

def set_cached_platform(show_name, platform, tmdb_id=None, season=None, episode=None):
    cache = load_platform_cache()
    name = show_name.lower()

    if name not in cache:
        cache[name] = {
            "platform": platform,
            "tmdb_id": tmdb_id,
            "timestamp": int(time.time())
        }

    if season and episode:
        ep_key = f"s{season}e{episode}"
        if "episodes" not in cache[name]:
            cache[name]["episodes"] = {}
        cache[name]["episodes"][ep_key] = {
            "platform": platform,
            "tmdb_id": tmdb_id,
            "timestamp": int(time.time())
        }

    save_platform_cache(cache)
