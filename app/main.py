from importlib import import_module
import pkgutil
from core.stt_tts import listen, speak

# Auto-load all plugins from the plugins/ directory
PLUGINS = {
    name: f"plugins.{name}"
    for _, name, _ in pkgutil.iter_modules(["plugins"])
}

def main():
    speak("Ready for your command.")
    while True:
        try:
            query = listen().lower()  # Convert query to lowercase for consistency
            
            # Let each plugin decide if it should handle the query
            handled = False
            for plugin_name, plugin_path in PLUGINS.items():
                try:
                    plugin = import_module(plugin_path)
                    if plugin.should_handle(query):
                        plugin.handle(query)
                        handled = True
                        break
                except Exception as e:
                    print(f"Plugin {plugin_name} failed: {str(e)}")
            
            if not handled:
                speak("Sorry, I didn't understand. Try again.")

        except KeyboardInterrupt:
            speak("Goodbye!")
            break
        except Exception as e:
            speak("An error occurred. Restarting...")
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
