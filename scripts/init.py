import os
import json

def ask(key, default=""):
    val = input(f"{key} [{default}]: ").strip()
    return val if val else default

def main():
    print("=== SARAH Setup Wizard ===\n")

    env = {
        "GROQ_API_KEY": ask("GROQ_API_KEY"),
        "GROQ_MODEL": ask("GROQ_MODEL", "llama3-8b-8192"),

        "TMDB_KEY": ask("TMDB_KEY"),
        "PLEX_SERVER": ask("PLEX_SERVER", "http://192.168.1.X:32400"),
        "PLEX_TOKEN": ask("PLEX_TOKEN"),
        "ONN_DEVICE_IP": ask("ONN_DEVICE_IP", "192.168.1.Y"),

        "HOME_ASSISTANT_URL": ask("HOME_ASSISTANT_URL", "http://homeassistant.local:8123"),
        "HOME_ASSISTANT_TOKEN": ask("HOME_ASSISTANT_TOKEN"),

        "MATTER_NODE_ID": ask("MATTER_NODE_ID", "1234"),
        "MATTER_LIGHT_ENDPOINT": ask("MATTER_LIGHT_ENDPOINT", "1"),

        "MQTT_BROKER": ask("MQTT_BROKER", "localhost"),
        "MQTT_PORT": ask("MQTT_PORT", "1883"),
        "MQTT_USERNAME": ask("MQTT_USERNAME"),
        "MQTT_PASSWORD": ask("MQTT_PASSWORD"),

        "ESP32_WS_URL": ask("ESP32_WS_URL", "ws://192.168.1.Z/ws")
    }

    print("\nWriting .env...")
    with open(".env", "w") as f:
        for k, v in env.items():
            f.write(f"{k}={v}\n")

    print("Writing platform_priority.json...")
    os.makedirs("configs", exist_ok=True)
    default_priority = {
        "arrested development": ["netflix", "hulu"],
        "*": ["tubi", "plex", "netflix"]
    }
    with open("configs/platform_priority.json", "w") as f:
        json.dump(default_priority, f, indent=2)

    print("Creating empty show_platform_cache.json...")
    with open("configs/show_platform_cache.json", "w") as f:
        json.dump({}, f)

    print("\nSetup complete! You can now start SARAH.")

if __name__ == "__main__":
    main()
